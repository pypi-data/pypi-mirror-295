import unittest
from cronos_chain_client.client import create_client

class TestClient(unittest.TestCase):
    def test_get_crc20_token_list(self):
        client = create_client({
            'chain': 'evm',
            'network': 'mainnet',
            'explorer': {
                'apiKey': 'r0B1D9QdhCPVR6EPvBg6yVLv7KTcypAF',
            }
        })

        # Test if the tokens list can be accessed through client.tokens.getCRC20TokenList()
        tokens = client.tokens.getCRC20TokenList()
        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)
        self.assertIn('name', tokens[0])
        self.assertIn('symbol', tokens[0])
        self.assertIn('contract_address', tokens[0])

if __name__ == '__main__':
    unittest.main()
