from django.shortcuts import render
from django.http import JsonResponse
from .models import CardData
from django.views.decorators.csrf import csrf_exempt
from .eth_operations import connect_to_ethereum_node, load_contract, get_account_from_card, process_shop_transaction, \
    deposit_tokens, get_balance_as_number
import json


def base(request):
    # base
    return render(request, 'helpfinance/base.html')


def dashboard(request):
    # dashboard
    return render(request, 'helpfinance/dashboard.html')


def display_data(request):
    # Fetch the data from the database
    card_data = CardData.objects.all()
    print(card_data)  # Print the fetched data
    # Pass the data to the template
    return render(request, 'helpfinance/display_data.html', {'card_data': card_data})


@csrf_exempt
def api_receive_data(request):
    if request.method == 'POST':
        if request.body:  # Check if the request body is not empty
            data = json.loads(request.body)
            # Store the data in the database
            card_data = CardData(id=data['id'], text=data['text'])
            card_data.save()
            print(card_data)  # Print the saved data
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed', 'error': 'Empty request body'})
    else:
        return JsonResponse({'status': 'failed', 'error': 'Invalid request method'})


def get_products():
    return [
        {'id': 1, 'name': 'Product 1', 'price': 10},
        {'id': 2, 'name': 'Product 2', 'price': 20},
        {'id': 3, 'name': 'Product 3', 'price': 30},
    ]


def sell_product(request, product_id):
    # connect to the Ethereum node
    w3 = connect_to_ethereum_node()
    contract = load_contract(w3)
    # get the card data from the Raspberry Pi
    card_data = get_account_from_card()
    # get the products from the products function
    products = get_products()
    # If product_id is 0, handle custom price, else find product and get its price
    if product_id == 0:
        amount_owed = float(request.POST.get('price', '0'))
    else:
        product = next((product for product in products if product['id'] == product_id), None)
        if product is None:
            return JsonResponse({'status': 'failed', 'error': 'Invalid product ID'})
        amount_owed = product['price']
    # Process the shop transaction and convert the transaction hash to a string
    txn_hash = process_shop_transaction(w3, contract, product_id, card_data, amount_owed)
    txn_hash_str = txn_hash.hex()
    # Return the transaction hash
    return JsonResponse({'transaction_hash': txn_hash_str})


def products(request):
    products = get_products()
    return render(request, 'helpfinance/products.html', {'products': products})


def ethereum_demo(request):
    # Connect to the Ethereum node and load the contract
    w3 = connect_to_ethereum_node()
    contract = load_contract(w3)

    # Get all accounts
    all_accounts = w3.eth.accounts

    # Render the ethereum_demo page and pass the accounts and contract to the template
    return render(request, 'helpfinance/ethereum_demo.html', {'accounts': all_accounts, 'contract': contract})


@csrf_exempt
def deposit_tokens_view(request, account):
    if request.method in ['GET', 'POST']:
        w3 = connect_to_ethereum_node()
        contract = load_contract(w3)
        # Distributor account
        distributor_account = w3.eth.accounts[0]
        deposit_tokens(w3, contract, distributor_account, account)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed', 'error': 'Invalid request method'})


def get_user_balance(request):
    # Connect to the Ethereum node and load the contract
    w3 = connect_to_ethereum_node()
    contract = load_contract(w3)
    # Get the account from the card
    account = get_account_from_card()
    # Get the balance of the account
    balance = get_balance_as_number(request, account)
    return JsonResponse({'balance': str(balance)})


from django.shortcuts import render

def donate_view(request):
    return render(request, 'helpfinance/donate.html')