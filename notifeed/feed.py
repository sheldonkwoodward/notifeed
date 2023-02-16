from notifeed.post import Post

TYPE_RSS = "rss"


class Feed:
    def __init__(self, identifier, config, databases):
        self.identifier = identifier
        self.enabled = config["enabled"]
        self.type = config["type"]

        if self.type == TYPE_RSS:
            self.rss_config = {
                "url": config["url"]
            }
            self.reader = databases["reader"]
        else:
            raise Exception(f"Unknown feed type '{self.type}'")

    def get_latest_posts(self):
        if not self.enabled:
            return []

        if self.type == TYPE_RSS:
            return self._get_latest_posts_rss()

        raise Exception(f"Unknown feed type '{self.type}'")

    def _get_latest_posts_rss(self):
        feed_url = self.rss_config["url"]

        # add and update the feed
        self.reader.add_feed(feed_url, exist_ok=True)
        self.reader.update_feed(feed_url)

        # process all unread feed posts
        entries = self.reader.get_entries(feed=feed_url, read=False)
        posts = []
        for entry in entries:
            posts.append(Post(entry.title, entry.get_content().value, url=entry.link, html=entry.get_content().is_html))
            self.reader.mark_entry_as_read(entry)

        return posts
