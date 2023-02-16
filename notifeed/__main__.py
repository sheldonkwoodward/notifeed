from collections import defaultdict
import json
import logging as log
import os
import sys
import time

from reader import make_reader

from notifeed.feed import Feed
from notifeed.matcher import Matcher
from notifeed.notifier import Notifier
from notifeed.search import Search


DEFAULT_CONFIG_FILE = "config.json"


def main():
    # load the config file
    config_file = os.getenv("CONFIG_FILE", DEFAULT_CONFIG_FILE)
    try:
        with open(config_file) as json_file:
            config = json.load(json_file)
    except FileNotFoundError as e:
        log.error("Could not load " + config_file)
        sys.exit(1)

    # parse the config
    databases = {
        "reader": make_reader(os.getenv(config["databases"]["reader_env"]))
    }

    feeds = {}
    for identifier, feed_config in config["feeds"].items():
        feeds[identifier] = Feed(identifier, feed_config, databases)

    matchers = {}
    for identifier, matcher_config in config["matchers"].items():
        matchers[identifier] = Matcher(identifier, matcher_config)

    notifiers = {}
    for identifier, notifier_config in config["notifiers"].items():
        notifiers[identifier] = Notifier(identifier, notifier_config)

    # TODO: investigate not having a special search object
    searches = {}
    for identifier, search_config in config["searches"].items():
        searches[identifier] = Search(identifier, search_config, feeds, matchers, notifiers)
        pass

    # determine which searches apply to which feeds
    feed_to_searches = defaultdict(lambda: set())
    for search in searches.values():
        for feed in search.feeds:
            feed_to_searches[feed.identifier].add(search.identifier)

    # start the loop to scan the feeds periodically
    while True:
        # iterate over all feeds
        for feed_identifier, feed in feeds.items():
            # get the latest entries for the feed
            log.info(f"Start searching feed '{feed_identifier}'")
            entries = feed.get_latest_entries()
            log.info(f"Got {len(entries)} new entries")

            # iterate over all applicable searches for the feed
            search_identifiers = feed_to_searches[feed_identifier]
            for search_identifier in search_identifiers:
                # search the feed's latest entries for a match
                log.info(f"Apply search '{search_identifier}' to the new entries")
                searches[search_identifier].match_and_notify(entries)

        # TODO: implement real task scheduling with wait time based on config
        log.info("Sleep for 60 seconds")
        time.sleep(60)

if __name__ == "__main__":
    log.basicConfig(stream=sys.stdout, level=log.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    main()
