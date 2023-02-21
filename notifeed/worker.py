import logging as log

def worker_main(job_queue):
    while True:
        queue_item = job_queue.get()
        job_func = queue_item[0]
        job_args = queue_item[1:]
        job_func(*job_args)
        job_queue.task_done()

def search_feed(feed_identifier, feed, feed_to_searches, searches):
    log.info(f"Start searching feed '{feed_identifier}'")
    posts = feed.get_latest_posts()
    log.info(f"Got {len(posts)} new posts")

    # iterate over all applicable searches for the feed
    search_identifiers = feed_to_searches[feed_identifier]
    for search_identifier in search_identifiers:
        # search the feed's latest posts for a match
        log.info(f"Apply search '{search_identifier}' to the new posts")
        searches[search_identifier].match_and_notify(posts)
