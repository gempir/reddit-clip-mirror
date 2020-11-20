# -*- coding: utf-8 -*-
"""
Twitch clips to streamable

@author: king344
"""
import os.path
from os import path
import re
 
import json
import praw

reddit = praw.Reddit(
    client_id="***REMOVED***",
    client_secret="***REMOVED***",
    user_agent="***REMOVED***",
    username="***REMOVED***",
    password="***REMOVED***"
)

import spaw  

SPAW = spaw.SPAW()

SPAW.auth('***REMOVED***', '***REMOVED***')

regex = r"https:\/\/(www|clips)\.twitch\.tv\/(\w*\/)?(clip\/)?\w*"

def check_condition(c):
    text = c.body

    match = re.search(r"https:\/\/(www|clips)\.twitch\.tv\/(\w*\/)?(clip\/)?\w*", text)
    if match and match.group():
        return match.group()
    else:
        return False

def save_json(data):
    with open('comments.json', 'w') as outfile:
        json.dump(data, outfile)

def load_json():
    with open('comments.json') as json_file:
        return json.load(json_file)

def main():
    if path.exists("comments.json"):
        cache = {} # load_json()
    else:
        cache = {}

    for c in reddit.subreddit("nnystest").comments():
        if c.id in cache:
            break
        else:
            url = check_condition(c)
            cache[c.id] = url
            save_json(cache)
            if url:
                stlink = SPAW.videoImport(url)
                newlink = 'https://streamable.com/'           
                newlink += stlink['shortcode']
                newlink += " I'm a bot bipp bopp!"
                c.reply(newlink)

if __name__ == "__main__":
    main()
