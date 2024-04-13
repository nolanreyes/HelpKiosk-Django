import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HelpKiosk.settings')

from web3 import Web3, HTTPProvider
import json

# Connect to the Ethereum node
w3 = Web3(HTTPProvider(settings.ETHEREUM_NODE_URL))

# Load the ABI
with open('helpfinance/contracts/builds/Deploy#HELPToken.json', 'r') as f:
    contract_data = json.load(f)
    contract_abi = contract_data['abi']

# The address of your deployed contract
contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# The address of your account (you need to have the private key to sign transactions)
my_address = '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'

# The private key of your account (NEVER share this with anyone)
my_private_key = 'ac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80'

# The address of a retailer
retailer_address = '0x70997970C51812dc3A010C7d01b50e0d17dc79C8'

# Deposit 10 Ether to your account
amount = w3.toWei(10, 'ether')
txn = contract.functions.deposit(my_address, amount).buildTransaction({
    'from': my_address,
    'nonce': w3.eth.getTransactionCount(my_address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')
})
signed_txn = w3.eth.account.signTransaction(txn, my_private_key)
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
w3.eth.waitForTransactionReceipt(txn_hash)

# Check the balance of your account
balance = contract.functions.getBalance(my_address).call()
print(f'Balance of my account: {balance} Wei')

# Spend 1 Ether at the retailer
amount = w3.toWei(1, 'ether')
txn = contract.functions.spendFunds(retailer_address, amount).buildTransaction({
    'from': my_address,
    'nonce': w3.eth.getTransactionCount(my_address),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')
})
signed_txn = w3.eth.account.signTransaction(txn, my_private_key)
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
w3.eth.waitForTransactionReceipt(txn_hash)

# Check the balance of the retailer
balance = contract.functions.getRetailerBalance(retailer_address).call()
print(f'Balance of the retailer: {balance} Wei')
