TYPE_RSS = "rss"


class Feed:
    def __init__(self, identifier, config, databases):
        self.identifier = identifier
        self.enabled = config["enabled"]
        self.type = config["type"]

        if self.type == TYPE_RSS:
            self.rss_config = config["config"]
            self.reader = databases["reader"]
        else:
            raise Exception(f"Unknown feed type '{self.type}'")

    def get_latest_entries(self):
        if not self.enabled:
            return []

        if self.type == TYPE_RSS:
            return self._get_latest_entries_rss()

        raise Exception(f"Unknown feed type '{self.type}'")

    def _get_latest_entries_rss(self):
        feed_url = self.rss_config["url"]
        check_content = self.rss_config["check_content"]

        # add and update the feed
        self.reader.add_feed(feed_url, exist_ok=True)
        self.reader.update_feed(feed_url)

        # process all unread feed entries
        entries = self.reader.get_entries(feed=feed_url, read=False)
        entries_prepped = []
        for entry in entries:
            entry_prepped = entry.title if not check_content else entry.title + "\n" + entry.get_content().value
            entries_prepped.append(entry_prepped)
            self.reader.mark_entry_as_read(entry)

        return entries_prepped
