from collections import defaultdict
import json
import logging as log
import os
import sys
import time

from jsonschema import validate, ValidationError
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
    except FileNotFoundError:
        log.error(f"Could not load config file '{config_file}'")
        sys.exit(1)

    # validate the schema against the JSON config if enabled
    if os.getenv("VALIDATE_CONFIG_SCHEMA", 'true').lower() in ('true', '1', 't'):
        # load the json schema
        schema_file = os.getenv("CONFIG_SCHEMA_FILE")
        try:
            with open(schema_file) as json_file:
                schema = json.load(json_file)
        except FileNotFoundError:
            log.error(f"Could not load config schema file '{schema_file}'")
            sys.exit(1)

        # validate the config against the schema
        try:
            validate(instance=config, schema=schema)
        except ValidationError as e:
            log.error("Config file is not valid")
            raise e

        log.info("Config file is valid")
    else:
        log.warning("Skipping validation for Config file")

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
            # get the latest posts for the feed
            log.info(f"Start searching feed '{feed_identifier}'")
            posts = feed.get_latest_posts()
            log.info(f"Got {len(posts)} new posts")

            # iterate over all applicable searches for the feed
            search_identifiers = feed_to_searches[feed_identifier]
            for search_identifier in search_identifiers:
                # search the feed's latest posts for a match
                log.info(f"Apply search '{search_identifier}' to the new posts")
                searches[search_identifier].match_and_notify(posts)

        # TODO: implement real task scheduling with wait time based on config
        log.info("Sleep for 60 seconds")
        time.sleep(60)

if __name__ == "__main__":
    log.basicConfig(stream=sys.stdout, level=log.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    main()
