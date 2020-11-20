# -*- coding: utf-8 -*-
"""
Twitch clips to streamable

@author: king344
"""

from urlextract import URLExtract

import os.path
from os import path
 
import numpy as np
from numpy import asarray
from numpy import savetxt
from numpy import loadtxt

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

def check_condition(c):
    text = c.body
    if "https://clips.twitch.tv/" in text:
        return True
    else:
        return False

def main():
    if path.exists("cache.csv"):
       cache = loadtxt('cache.csv', delimiter=',')
    else:
        cache = asarray([])
    while True:
        for c in reddit.subreddit("nnystest").comments():
            if c.id in cache:
                break
            else:
                cache = np.append(cache, c.id)
                savetxt('data.csv', cache, delimiter=',')
                condition = check_condition(c)
                if condition:
                    extractor = URLExtract()
                    urls = extractor.find_urls(c.body)
                    twitchlink = urls[0]
                    stlink = SPAW.videoImport(twitchlink)          
                    newlink = 'https://streamable.com/'           
                    newlink += stlink['shortcode']
                    newlink += " I'm a bot bipp bopp!"
                    c.reply(newlink)

if __name__ == "__main__":
    main()
