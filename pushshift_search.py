import praw
from psaw import PushshiftAPI
import datetime as dt
import json
import os
import sys
from pathlib import Path

with open("auth.json", "r") as auth_file:
    auth = json.load(auth_file)

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    
reddit = praw.Reddit(**auth)
psapi = PushshiftAPI(reddit)

print(type(config['subreddits']))
sub_names = ','.join(config['subreddits'])

def parse_comment(comment):
    return {
        #"author": comment.author.name if comment.author is not None else "[deleted]",
        #"author_fullname": comment.author_fullname,
        #"num_comments": comment.num_comments,
        "body": comment.body,
        #"created_utc": comment.created_utc,
        #"id": comment.id,
        #"link_id": comment.link_id,
        #"parent_id": comment.parent_id,
        #"score": comment.score,
        #"subreddit_id": comment.subreddit_id,
        #"subreddit": comment.subreddit.display_name
    }

start_date = int(dt.datetime(config["start_year"], config["start_month"], config["start_day"]).timestamp())
#end_date = int(dt.datetime.today().timestamp())
end_date = int(dt.datetime(config["end_year"], config["end_month"], config["end_day"]).timestamp())

#https://en.m.wikipedia.org/wiki/List_of_designer_drugs
#https://www.drugsdata.org/ 

Path(config["save_folder"]).mkdir(exist_ok=True)

for reddit in config['subreddits']:
    print("Starting", reddit)

    gen = psapi.search_comments(
        subreddit=reddit,
        after=start_date,
        before=end_date,
        fields='body'
        #aggs="created_utc",
        #frequency="day",
    )

    data = [comment.body for comment in gen]

    print("found", len(data), "results")

    with open(os.path.join(config["save_folder"], reddit+'.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
