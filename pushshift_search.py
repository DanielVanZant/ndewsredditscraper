import praw
from psaw import PushshiftAPI
import datetime as dt
import json

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    
reddit = praw.Reddit(**config['auth'])
psapi = PushshiftAPI(reddit)

sub_names = ','.join(config['subreddits'])

start_date = int(dt.datetime(2019, 1, 1).timestamp())
end_date = int(dt.datetime(2020, 9, 23).timestamp())

results_dict = {}
for keyword in config['keywords']:
    gen = psapi.search_comments(
        q=keyword, 
        subreddit='researchchemicals',
        after=start_date,
        before=end_date
        #aggs="created_utc",
        #frequency="day",
    )

    results_dict[keyword] = list(gen)