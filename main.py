import os.path
from os import path
import re
import logging

import json
import praw

import requests

logging.basicConfig(
    filename='process.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

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

    match = re.search(
        r"https:\/\/(www|clips)\.twitch\.tv\/(\w*\/)?(clip\/)?\w*", text)
    if match and match.group():
        return match.group()
    else:
        return False


def main():
    postsid = ['jxr1p8', 'jxqvez', 'jxrmcl', 'jxrn3p', 'jxr0sb', 'jxqoip',
               'jxraoe', 'jxqnwf', 'jxqgr8', 'jxqkpt', 'jxqjhh', 'jxqgj4', 'jxqers']

    for post in postsid:
        submission = reddit.submission(id=post)
        submission.comments.replace_more(limit=None)

        logging.info("Processing {} comments".format(len(submission.comments)))
        for c in submission.comments:
            url = check_condition(c)
            already_replied = False

            if len(c.replies) > 0:
                for reply in c.replies:
                    if reply.author.name == cfg['username']:
                        logging.info("Already replied to " + c.id)
                        already_replied = True
                        break

            if url and not already_replied:
                link = uploadToStreamable(url)
                if link:
                    c.reply("Mirror: " + link)


def uploadToStreamable(url):
    try:
        response = requests.get('https://api.streamable.com/import?url=' +
                                url, auth=(cfg['streamableEmail'], cfg['streamablePassword']))
        if response.status_code == 200:
            data = response.json()
            logging.info("Success uploading: " + url +
                         " id: " + data['shortcode'])
            return "http://streamable.com/" + data['shortcode']
        else:
            logging.error(response.text)
            return False
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return False


if __name__ == "__main__":
    main()
