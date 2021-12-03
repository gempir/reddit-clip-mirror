import logging
import os
import sys

import praw

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent="botnextdoor by /u/gempir github.com/gempir/reddit-clip-mirror",
    username=os.getenv('REDDIT_USERNAME'),
    password=os.getenv('REDDIT_PASSWORD')
)

comment = sys.argv[1:][0]
link = sys.argv[1:][1]
title = sys.argv[1:][2]

try:
    c = reddit.comment(comment)
    print(f"Replying to {comment}: Mirror {title} {link}")
    c.reply(f"Mirror:\n{title}\n{link}")
except Exception as e:
    logging.error(e)
