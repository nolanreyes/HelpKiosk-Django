from django.http import HttpResponse
from web3 import Web3, HTTPProvider
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.conf import settings


def test_connection(request):
    w3 = connect_to_ethereum_node()
    if w3.is_connected():
        return HttpResponse('Connected to the blockchain')
    else:
        return HttpResponse('Connection to the blockchain failed')


def connect_to_ethereum_node():
    # Connect to the Ethereum node
    w3 = Web3(HTTPProvider(settings.ETHEREUM_NODE_URL))
    return w3


def load_contract(w3):
    # Load the ABI
    with open('helpfinance/contracts/builds/Deploy#HELPToken.json', 'r') as f:
        contract_data = json.load(f)
        contract_abi = contract_data['abi']
    # The address of your deployed contract
    contract_address = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
    # Create a contract instance
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    return contract


def deposit_tokens(w3, contract, distributor_account, user_account):
    # deposit 10 hTKN to each user account from the distributor account when used
    amount = Web3.to_wei(10, 'ether')
    txn_hash = contract.functions.deposit(user_account, amount).transact({
        'from': distributor_account,
        'nonce': w3.eth.get_transaction_count(distributor_account),
        'gas': 1728712,
        'gasPrice': Web3.to_wei('21', 'gwei'),
        'chainId': 31337  
    })
    w3.eth.wait_for_transaction_receipt(txn_hash)


def get_balance(request, account):
    w3 = connect_to_ethereum_node()
    contract = load_contract(w3)
    # Check the balance of each user account and convert it to hTKN
    balance = float(Web3.from_wei(contract.functions.getBalance(account).call(), 'ether'))
    return JsonResponse({'balance': balance})


def get_balance_as_number(request, account):
    response = get_balance(request, account)
    balance = json.loads(response.content)['balance']
    return balance


@csrf_exempt
def contract_interaction(request, account):
    if request.method == 'POST':
        w3 = connect_to_ethereum_node()
        contract = load_contract(w3)
        # Distributor account
        distributor_account = w3.eth.accounts[0]
        deposit_tokens(w3, contract, distributor_account, account)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'error': 'Invalid request method'})


def get_account_from_card():
    # Local IP address of the Raspberry Pi for testing purposes
    #url = 'http://192.168.0.185:5000/read_card'

    # TUD IP address of the Raspberry Pi
    url = 'http://10.156.34.61:5000/read_card'

    # Public URL of the Raspberry Pi using ngrok for accessing from external networks
    # url = 'http://surely-direct-jennet.ngrok-free.app/read_card'

    # Send a GET request to the Raspberry Pi endpoint
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to get card data from Raspberry Pi: {response.content}")
    # The response content  contains the account address
    data = json.loads(response.content)
    # extract the account address
    account = data['text'].strip()
    if account is None:
        raise Exception("Failed to retrieve account from card data")
    return account


def process_transaction(w3, contract, shop_account, card_data, amount_owed):
    # retrieve the user account from the card data
    user_account = get_account_from_card()
    # convert the amount to wei
    amount = Web3.to_wei(amount_owed, 'ether')
    # create a transaction from the user account to the shop account
    txn_hash = contract.functions.transfer(shop_account, amount).transact({
        'from': user_account,
        'nonce': w3.eth.get_transaction_count(user_account),
        'gas': 1728712,
        'gasPrice': Web3.to_wei('21', 'gwei'),
        'chainId': 31337  # Replace with your network's chain ID
    })
    # wait for the transaction to be mined
    w3.eth.wait_for_transaction_receipt(txn_hash)
    return txn_hash


def get_shop_account():
    # For now, just return this account
    return '0x8626f6940E2eb28930eFb4CeF49B2d1F2C9C1199'  


def process_shop_transaction(w3, contract, product_id, card_data, amount_owed):
    # Get the shop account
    shop_account = get_shop_account()
    # Process the transaction
    txn_hash = process_transaction(w3, contract, shop_account, card_data, amount_owed)
    return txn_hash
