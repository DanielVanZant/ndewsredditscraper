import praw
import json
import time

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    
reddit = praw.Reddit(**config['auth'])

def build_multireddit(sub_list):
    return "+".join(sub_list)

sub_names = build_multireddit(config['subreddits'])
subreddit = reddit.subreddit(sub_names)

def parse_comment(comment):
    return {
        "author": comment.author.name,
        "author_fullname": comment.author_fullname,
        "num_comments": comment.num_comments,
        "body": comment.body,
        "created_utc": comment.created_utc,
        "id": comment.id,
        "link_id": comment.link_id,
        "parent_id": comment.parent_id,
        "score": comment.score,
        "subreddit_id": comment.subreddit_id,
        "subreddit": comment.subreddit.display_name
    }

for comment in subreddit.stream.comments():
    props = parse_comment(comment)
    print(props)

