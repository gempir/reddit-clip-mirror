import logging
import os
import re

import praw
import requests

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

def check_condition(c):
    text = c.body

    match = re.search(
        r"\bhttps?:\/\/((clips|m)\.twitch\.tv\/?\/?(clip)?|www\.twitch\.tv\/([A-z\d_]+)?\/clip)\/[A-z]+(-[A-z\d_-]{16})?\b", text)
    if match and match.group():
        return match.group()
    else:
        return False


def main():
    postsid = ['qmm84u']
    logging.info(f"Scanning {len(postsid)} posts")

    for post in postsid:
        submission = reddit.submission(id=post)
        submission.comments.replace_more(limit=None)

        logging.info(f"Processing {len(submission.comments)} comments on post {submission.name}")
        for c in submission.comments:
            url = check_condition(c)
            already_replied = False

            if len(c.replies) > 0:
                for reply in c.replies:
                    if reply.author.name == os.getenv('REDDIT_USERNAME'):
                        already_replied = True
                        break

            if url and not already_replied:
                logging.info(f"Found new clip: {url}")
                link = uploadToStreamable(url)
                if link:
                    logging.info("Replying {}: Mirror: {}".format(c.id, link))
                    c.reply("Mirror: {}".format(link))


def uploadToStreamable(url):
    try:
        response = requests.get('https://api.streamable.com/import?url=' +
                                url, auth=(os.getenv('STREAMABLE_EMAIL'), os.getenv('STREAMABLE_PASSWORD')))
        if response.status_code == 200:
            data = response.json()
            logging.info("Success uploading: " + url +
                         " id: " + data['shortcode'])
            return "http://streamable.com/" + data['shortcode']
        else:
            logging.error("Streamable error {} {}".format(response.status_code, response.text))
            return False
    except requests.exceptions.RequestException as e:
        logging.error(e)
        return False


if __name__ == "__main__":
    main()
