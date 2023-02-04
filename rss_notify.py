import json
import logging as log
import os
import sys
import time

from reader import make_reader
import requests

log.basicConfig(stream=sys.stdout, level=log.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

PUSHOVER_URL = 'https://api.pushover.net/1/messages.json'

CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.json')
DATABASE_FILE = os.getenv('DATABASE_FILE', 'db.sqlite')
UPDATE_INTERVAL_SECONDS = int(os.getenv('UPDATE_INTERVAL_SECONDS', 60))
PUSHOVER_USER = os.getenv('PUSHOVER_USER')
PUSHOVER_TOKEN = os.getenv('PUSHOVER_TOKEN')

def process_entry(entry, feed_config):
    log.info(f'Processing entry {entry.title}')

    check_content = feed_config.get('check_content', True)
    match_all_words = feed_config.get('match_all', [])
    match_some_words = feed_config.get('match_some', [])
    pushover_priority = feed_config.get("pushover_priority", 0)

    search_text = entry.title.casefold()
    if check_content:
        search_text += entry.get_content().value.casefold()

    if match_all_words is not None and len(match_all_words) > 0:
        # check if all required words are in the entry
        match_all = True
        for word in match_all_words:
            word_prepped = word.casefold()
            match_all = match_all and word_prepped in search_text

        # stop processing if the entry does not match all the required words
        if not match_all:
            return

    if match_some_words is not None and len(match_some_words) > 0:
        # check that at least one optional word is in the entry
        match_some = False
        for word in match_some_words:
            word_prepped = word.casefold()
            match_some = match_some or word_prepped in search_text

            if match_some:
                break

        # stop processing if the entry does not match any of the optional words
        if not match_some:
            return

    # send a notification for the matching entry
    log.info(f'Send notification for entry {entry.title}')
    log.info(f'Entry link {entry.link}')
    params = {
        'user': PUSHOVER_USER,
        'token': PUSHOVER_TOKEN,
        'title': entry.title,
        'message': entry.get_content().value,
        'url': entry.link,
        'html': int(entry.get_content().is_html),
        'priority': pushover_priority
    }
    requests.post(PUSHOVER_URL, params)

def process_feed(reader, feed_url, feed_config):
    log.info(f'Processing feed {feed_url}')

    # add and update the feed
    reader.add_feed(feed_url, exist_ok=True)
    reader.update_feed(feed_url)

    # process all unread feed entries
    entries = reader.get_entries(feed=feed_url, read=False)
    for entry in entries:
        process_entry(entry, feed_config)
        reader.mark_entry_as_read(entry)

def main():
    # validate the pushover key and token
    if PUSHOVER_USER is None:
        log.error('Environment variable PUSHOVER_USER is not defined')
        sys.exit(1)
    if PUSHOVER_TOKEN is None:
        log.error('Environment variable PUSHOVER_TOKEN is not defined')
        sys.exit(1)

    # load the config file
    try:
        with open(CONFIG_FILE) as json_file:
            config = json.load(json_file)
    except FileNotFoundError as e:
        log.error('Could not load ' + CONFIG_FILE)
        sys.exit(1)

    # setup the reader DB
    reader = make_reader(DATABASE_FILE)

    # start the loop to scan the RSS feeds
    while True:
        for feed_url, feed_config in config.items():
            if feed_config['enabled']:
                process_feed(reader, feed_url, feed_config)

        log.info(f'Sleep for {UPDATE_INTERVAL_SECONDS} seconds')
        time.sleep(UPDATE_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
