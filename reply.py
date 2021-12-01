from __future__ import unicode_literals

import json
import logging
import os
import re

import praw
import youtube_dl
from mega import Mega

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

mega = Mega()
m = mega.login(os.getenv('MEGA_USERNAME'), os.getenv('MEGA_PASSWORD'))


with open('replies.json') as fd:
    replies = json.load(fd)

    for reply in replies:
        c = reddit.comment(reply['comment'])
        print(c.body)

        public_link = m.export("nnys2021clips/clips/" + reply['file'].lstrip("./"))
        print(public_link + " new mega link")



