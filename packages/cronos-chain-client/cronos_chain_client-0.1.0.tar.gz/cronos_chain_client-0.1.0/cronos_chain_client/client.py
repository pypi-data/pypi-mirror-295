from cronos_chain_client.tokens import Tokens

class Client:
    def __init__(self, chain, network, explorer):
        self.chain = chain
        self.network = network
        self.explorer = explorer
        self.tokens = Tokens(chain, network)  

def create_client(config):
    """Factory function to create the client, similar to JavaScript's createClient."""
    return Client(
        chain=config.get('chain', 'evm'),
        network=config.get('network', 'mainnet'),
        explorer=config.get('explorer', {})
    )

