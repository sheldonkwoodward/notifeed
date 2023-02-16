import logging as log


class Search:
    def __init__(self, identifier, config, feeds, matchers, notifiers):
        self.identifier = identifier
        self.enabled = config["enabled"]

        # get the instantiated feeds
        self.feeds = []
        for feed_identifier in config["feeds"]:
            self.feeds.append(feeds[feed_identifier])

        # get the instantiated matchers
        self.matchers = []
        for matcher_identifier in config["matchers"]:
            self.matchers.append(matchers[matcher_identifier])

        # get the instantiated notifiers
        self.notifiers = []
        for notifier_identifier in config["notifiers"]:
            self.notifiers.append(notifiers[notifier_identifier])

    def match_and_notify(self, entries):
        if not self.enabled:
            log.info(f"Search {self.identifier} is disabled")
            return False

        for entry in entries:
            log.info(f"Processing entry '{entry}'")
            for matcher in self.matchers:
                if matcher.is_match(entry):
                    log.info("Match found, sending notifications")
                    for notifier in self.notifiers:
                        # TODO: proper entry title and message support with new Entry class
                        notifier.send_notification(entry, entry)
                    continue
