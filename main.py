import logging
import os
import re

import praw
import youtube_dl

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

cache = []

try: 
    cache_comment = reddit.comment(id='hn481ru')
    cache = cache_comment.body.split(",")
except Exception as e:
    logging.warning("Cache comment could not be fetched", exc_info=e)

def check_condition(c):
    text = c.body

    match = re.search(
        r"\bhttps?:\/\/((clips|m)\.twitch\.tv\/?\/?(clip)?|www\.twitch\.tv\/([A-z\d_]+)?\/clip)\/[A-z]+(-[A-z\d_-]{16})?\b", text)
    if match and match.group():
        return match.group()
    else:
        return False

def main():
    postsid = [
        'qy8dws',
        'qy8cyi',
        'qy8can',
        'qy8bgn',
        'qy8aty',
        'qv8fkg',
        'qv8djx',
        'qrpz57',
        'qrpyps',
        'qrpxih',
        'qrpwuf',
        'qrpvx8',
        'qrpv97',
        'qrpv46',
        'qrpstz',
        'qrpshr',
        'qrpsa6',
        'qrps1e',
        'qrprhr',
        'qrpq2w'
    ]

    logging.info(f"Scanning {len(postsid)} posts")

    for post in postsid:
        submission = reddit.submission(id=post)
        submission.comments.replace_more(limit=None)

        logging.info(f"Processing {len(submission.comments)} comments on post {submission.id}: {submission.title}")
        if submission.locked:
            logging.info(f"Post {submission.id}: {submission.title} is locked, skipping")
            continue

        for c in submission.comments:
            url = check_condition(c)
            already_replied = False

            if c.id in cache:
                continue

            if len(c.replies) > 0:
                for reply in c.replies:
                    if reply and reply.author and reply.author.name == os.getenv('REDDIT_USERNAME'):
                        already_replied = True
                        break

            if url and not already_replied:
                logging.info(f"Found new clip: {url}")
                saveClip(url, c)
                logging.info(f"{len(replies)} clips saved")
                if len(replies) >= 10:
                   save_and_exit() 
    
    save_and_exit()

def save_and_exit():
    logging.info("clips limit downloaded, exiting")
    with open('replies.txt', "w") as f:
        for line in replies:
            f.write(line + "\n")
    cache_comment.edit(",".join(cache))
    os._exit(0)

replies = []

def saveClip(url, c):
    title = ""

    try:
        def finished_upload(d):
            if d['status'] == 'finished':
                print(d['filename'] + ' Done downloading')
                replies.append(d['filename'].lstrip("./") + ";" + c.id + ";" + title)

        ydl_opts = {
            'progress_hooks': [finished_upload],
            'outtmpl': './clips/%(id)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            title = ydl.extract_info(url, download=False)['title']
            ydl.download([url])
       
    except Exception as e:
        cache.append(c.id)
        logging.error(e)


if __name__ == "__main__":
    main()
