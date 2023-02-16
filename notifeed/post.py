class Post:
    def __init__(self, title, message, url=None, html=False):
        self.title = title
        self.message = message
        self.url = url
        self.html = html

    def __str__(self):
        return self.title

    def get_match_text(self, check_title, check_message):
        match_text = ""

        if check_title:
            match_text += self.title

        if check_title and check_message:
            match_text += "\n"

        if check_message:
            match_text += self.message

        return match_text
