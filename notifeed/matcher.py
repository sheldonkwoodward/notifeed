TYPE_SUBSTRING = "substring"


class Matcher:
    def __init__(self, identifier, config):
        self.identifier = identifier
        self.type = config["type"]

        if self.type == TYPE_SUBSTRING:
            self.substring_config = config["config"]
        else:
            raise Exception(f"Unknown matcher type '{self.type}'")

    def is_match(self, match_text):
        if self.type == TYPE_SUBSTRING:
            return self._is_match_substring(match_text)

        raise Exception(f"Unknown matcher type '{self.type}'")

    def _is_match_substring(self, match_text):
        case_sensitive = self.substring_config["case_sensitive"]
        match_groups = self.substring_config["match_groups"]

        # make the match text case insensitive if specified in the config
        match_text_prepped = match_text if case_sensitive else match_text.casefold()

        # check the match text against each match group
        for group in match_groups:
            match_all = True
            # check if all the words in the match group are in the match text
            for word in group:
                # make the word case insensitive if specified and compare against the match text
                word_prepped = word if not case_sensitive else word.casefold()
                match_all = match_all and word_prepped in match_text_prepped

            # immediately return true if all words in the match group are found in the match text
            if match_all:
                return True

        # return false if none of the match groups matches the match text
        return False
