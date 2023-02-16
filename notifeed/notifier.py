import os
import requests


TYPE_PUSHOVER = "pushover"
URL_PUSHOVER = 'https://api.pushover.net/1/messages.json'


class Notifier:
    def __init__(self, identifier, config):
        self.identifier = identifier
        self.enabled = config["enabled"]
        self.type = config["type"]

        if self.type == TYPE_PUSHOVER:
            self.pushover_config = config["config"]
        else:
            raise Exception(f"Unknown notifier type '{self.type}'")

    def send_notification(self, post):
        if not self.enabled:
            return False

        if self.type == TYPE_PUSHOVER:
            return self._send_notification_pushover(post)

        raise Exception(f"Unknown notifier type '{self.type}'")

    def _send_notification_pushover(self, post):
        # throw an exception if the pushover user is not specified in an environment variable
        user_env = self.pushover_config["user_env"]
        user = os.getenv(user_env)
        if user is None:
            raise Exception(f"Pushover user environment variable '{user_env}' not found")

        # throw an exception if the pushover token is not specified in an environment variable
        token_env = self.pushover_config["token_env"]
        token = os.getenv(token_env)
        if token is None:
            raise Exception(f"Pushover token environment variable '{token_env}' not found")

        # assemble the pushover api request params
        params = {
            "user": user,
            "token": token,
            "title": post.title,
            "message": post.message,
            "html": int(post.html),
            "priority": self.pushover_config["priority"]
        }
        if post.url is not None:
            params["url"] = post.url

        # send the notification request to pushover
        requests.post(URL_PUSHOVER, params)
