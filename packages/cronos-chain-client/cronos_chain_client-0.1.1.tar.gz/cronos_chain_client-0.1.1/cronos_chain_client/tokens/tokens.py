import json
import os

class Tokens:
    def __init__(self, chain, network):
        self.chain = chain
        self.network = network
        self.token_list = self._load_token_list()

    def _load_token_list(self):
        """Loads the appropriate token list based on the chain and network."""
        # Define the path based on the chain and network
        filename = f"{self.network}/{self.chain}_token_list.json"
        token_list_path = os.path.join(os.path.dirname(__file__), filename)

        # Check if the file exists, raise an error if it doesn't
        if not os.path.exists(token_list_path):
            raise FileNotFoundError(f"Token list for {self.chain} on {self.network} network not found.")

        # Load the token list from the file
        with open(token_list_path, 'r') as f:
            return json.load(f)

    def getCRC20TokenList(self):
        """Returns the token list for the specified chain and network."""
        return self.token_list
