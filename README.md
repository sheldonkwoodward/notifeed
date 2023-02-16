# RSS Notify
A simple script to scan RSS feeds, look for keywords, and send notifications for matches through Pushover.

# Quick start
1. Create a new directory in the project root called `notifeed-data`
2. Copy the `config-example.json` to `notifeed-data/config.json`
3. Edit the config based on the configuration sections below
4. Copy the `example.env` to `.env`
5. Protect the file `chmod 600 .env`
6. Edit the `.env` to add your credentials
7. Run `docker-compose build && docker-compose up`

# Configuration JSON
**TODO**

# Configuration env variables
Along with the configuration JSON for the feeds to scan, the script has some required and optional environment
 variables:

**Required**
These environment variables are referenced by the config file. You can rename them to whatever you like, you will
 just need to ensure your `config.json` file matches the variables declared in the `docker-compose.yml` file.

* `PUSHOVER_USER` - The user key from Pushover used to send notifications
* `PUSHOVER_TOKEN` - The application token from Pushover used to send notifications
* `READER_DATABASE` (default `reader.sqlite`) - Name of the reader database file to load

**Optional**
* `CONFIG_FILE` (default `config.json`) - Name of the configuration file to load
