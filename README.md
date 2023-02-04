# RSS Notify
A simple script to scan RSS feeds, look for keywords, and send notifications for matches through Pushover.

# Non-docker quick start
1. Install the dependencies `pipenv install`
2. Copy the `config-example.json` to `config.json`
3. Follow the configuration instructions below to setup the script
4. Run the script with `pipenv run python rss_notify.py`

# Configuration JSON
The configuration is a JSON object. Each key is the feed's URL. The value of each key is the configuration object for
 that specific feed. The following values are allowed in the configuration object:

**Required**
* `enabled` - Boolean flag to determine if the feed should be scanned

**Optional**
* `check_content` (default `true`) - Boolean flag to determine if the content of the feed entry should be considered
 when checking the match words
* `match_all` (default `null`) - List of substrings that all must exist in the content being checked, if `null` then
 the match is considered successful
* `match_some` (default `null`) - List of substrings that at least one must in exist in the content being checked, if
 `null` then the match is considered successful
* `pushover_priority` (default `0`) - Pushover notification priority number, see Pushover documentation
 https://pushover.net/api

# Configuration env variables
Along with the configuration JSON for the feeds to scan, the script has some required and optional environment
 variables:

**Required**
* `PUSHOVER_USER` - The user key from Pushover used to send notifications
* `PUSHOVER_TOKEN` - The application token from Pushover used to send notifications

**Optional**
* `CONFIG_FILE` (default `config.json`) - Name of the configuration file to load
* `DATABASE_FILE` (default `db.sqlite`) - Name of the database file to load
* `UPDATE_INTERVAL_SECONDS` (default `60`) - Number of seconds to wait between scans
