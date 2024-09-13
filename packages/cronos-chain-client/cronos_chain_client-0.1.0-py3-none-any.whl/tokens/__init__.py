import json
import os

class Tokens:
    def __init__(self):
        self.token_list = self._load_token_list()

    def _load_token_list(self):
        """Loads the token list from the token_list.json file."""
        token_list_path = os.path.join(os.path.dirname(__file__), 'token_list.json')
        with open(token_list_path, 'r') as f:
            return json.load(f)

    def getCRC20TokenList(self):
        """Returns the hardcoded list of CRC20 tokens."""
        return self.token_list
