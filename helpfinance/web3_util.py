import os
from django.conf import settings
from web3 import Web3


# Connect to the local blockchain
def get_web3_connection():
    return Web3(Web3.HTTPProvider(settings.ETHEREUM_NODE_URL))


# connect to the local blockchain
w3 = get_web3_connection()

# Check the connection status
if w3.is_connected():
    print('Connected to the blockchain')
else:
    print('Connection to the blockchain failed')
