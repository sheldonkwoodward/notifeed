import logging as log


class Search:
    def __init__(self, identifier, config, feeds, matchers, notifiers):
        self.identifier = identifier
        self.enabled = config["enabled"]
        self.check_title = config["check_title"]
        self.check_message = config["check_message"]

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

    def match_and_notify(self, posts):
        if not self.enabled:
            log.info(f"Search {self.identifier} is disabled")
            return False

        for post in posts:
            log.info(f"Processing post '{post}'")
            for matcher in self.matchers:
                match_text = post.get_match_text(self.check_title, self.check_message)
                if matcher.is_match(match_text):
                    log.info("Match found, sending notifications")
                    for notifier in self.notifiers:
                        notifier.send_notification(post)
                    continue
