# -*- coding: utf-8 -*-
"""
Twitch clips to streamable

@author: king344
@author: gempir
"""
import os.path
from os import path
import re
import logging
 
import json
import praw

import requests

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def save_json(data):
    with open('comments.json', 'w') as outfile:
        json.dump(data, outfile)

def load_json(file):
    with open(file) as json_file:
        return json.load(json_file)

cfg = load_json("config.json")

reddit = praw.Reddit(
    client_id=cfg['clientId'],
    client_secret=cfg['clientSecret'],
    user_agent=cfg['userAgent'],
    username=cfg['username'],
    password=cfg['password']
)

regex = r"https:\/\/(www|clips)\.twitch\.tv\/(\w*\/)?(clip\/)?\w*"

def check_condition(c):
    text = c.body

    match = re.search(r"https:\/\/(www|clips)\.twitch\.tv\/(\w*\/)?(clip\/)?\w*", text)
    if match and match.group():
        return match.group()
    else:
        return False


def main():
    if path.exists("comments.json"):
        cache =  load_json("comments.json")
    else:
        cache = {}

    postsid = ['jxr1p8','jxqvez','jxrmcl','jxrn3p','jxr0sb','jxqoip','jxraoe','jxqnwf','jxqgr8','jxqkpt','jxqjhh','jxqgj4','jxqers']

    for post in postsid:
        submission = reddit.submission(id=post)
        for c in submission.comments:
            if c.id in cache:
                break
            else:
                url = check_condition(c)
                if url:
                    link = uploadToStreamable(url)
                    if link:
                        c.reply("Mirror: " + link)
                        cache[c.id] = link
                        save_json(cache)


def uploadToStreamable(url):
    try:
        response = requests.get('https://api.streamable.com/import?url='+url, auth=(cfg['streamableEmail'], cfg['streamablePassword']))
        if response.status_code == 200:
            data = response.json()
            logging.info("Success uploading: " + url + " id: " + data['shortcode'])
            return "http://streamable.com/" + data['shortcode']
        else: 
            logging.error(response.text)
            return False
    except requests.exceptions.RequestException as e:
        return str(e)

if __name__ == "__main__":
    main()
