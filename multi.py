# -*- coding: utf-8 -*-
"""
@author: King344
"""
import praw

cfg = load_json("config.json")

reddit = praw.Reddit(
    client_id=cfg['clientId'],
    client_secret=cfg['clientSecret'],
    user_agent=cfg['userAgent'],
    username=cfg['username'],
    password=cfg['password']
)

"""

POSTS ID

jxr1p8 > most_wholesome_moment_2020/

jxqvez > cringiest_moment_2020/

jxrmcl > best_tts_donation_2020/

jxrn3p > god_gamer_of_the_year/

jxr0sb > sexiest_moment_2020/

jxrnu6 > best_stream_snipe_2020/

jxqr0b > timing_of_the_year/

jxqoip > biggest_rage_moment_2020/

jxraoe > funniest_moment_on_twitch_2020/

jxqnwf > most_pepega_moment/

jxqgr8 > most_dansgame_moment_2020/

jxqkpt > most_5head_moment/

jxqjhh > biggest_failfish_moment/

jxqgj4 > most_pogchamp_moment_2020/

jxqers > scariest_moment_2020/

"""

postsid = ['jxr1p8','jxqvez','jxrmcl','jxrn3p','jxr0sb','jxqoip','jxraoe','jxqnwf','jxqgr8','jxqkpt','jxqjhh','jxqgj4','jxqers']

for post in postsid:
    submission = reddit.submission(id=post)
    for c in submission.comments:
        print(c)
