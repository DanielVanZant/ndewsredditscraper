import praw
from psaw import PushshiftAPI
import datetime as dt
import json
import os
import sys
import time

assert len(sys.argv) > 2
subreddit = sys.argv[1]
scrape_count = int(sys.argv[2])

with open("auth.json", "r") as auth_file:
    auth = json.load(auth_file)

reddit = praw.Reddit(**auth)
psapi = PushshiftAPI(reddit)

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

def get_timestamp():
    return str(int(time.time() * 1000))

scrapes_dir = "scrapes/"

gen = psapi.search_comments(
        subreddit=subreddit
    )

data = []
for i, comment in enumerate(gen, start=1):
    data.append(parse_comment(comment))
    if i >= scrape_count:
        break
    elif i % 1000 == 0:
        print(i)

fname = subreddit + "_" + get_timestamp() + ".json"
with open(os.path.join(scrapes_dir, fname), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)




