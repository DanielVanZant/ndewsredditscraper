import praw
from psaw import PushshiftAPI
import datetime as dt
import json
import os
import sys

keyword_list = None
if len(sys.argv) > 1:
    with open(sys.argv[1], "r") as f:
        keyword_list = f.read().split("\n")


downloads_dir = "downloads/"

with open("auth.json", "r") as auth_file:
    auth = json.load(auth_file)

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    
reddit = praw.Reddit(**auth)
psapi = PushshiftAPI(reddit)

sub_names = ','.join(config['subreddits'])

def parse_comment(comment):
    return {
        #"author": comment.author.name,
        #"author_fullname": comment.author_fullname,
        #"num_comments": comment.num_comments,
        "body": comment.body,
        "created_utc": comment.created_utc,
        "id": comment.id,
        "link_id": comment.link_id,
        "parent_id": comment.parent_id,
        "score": comment.score,
        "subreddit_id": comment.subreddit_id,
        "subreddit": comment.subreddit.display_name
    }

start_date = int(dt.datetime(2019, 1, 1).timestamp())
end_date = int(dt.datetime(2020, 9, 23).timestamp())

if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)

if keyword_list is None:
    keyword_list = config['keywords']

for keyword in keyword_list:
    print("Starting", keyword)

    gen = psapi.search_comments(
        q=keyword, 
        subreddit=sub_names,
        after=start_date,
        before=end_date
        #aggs="created_utc",
        #frequency="day",
    )

    data = [parse_comment(c) for c in gen]

    print("found", len(data), "results")

    with open(os.path.join(downloads_dir, keyword+'.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
