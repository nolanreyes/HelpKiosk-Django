# API caller

import requests
import json

def send_data_to_server(url, data):
    """
    Send data to the server.

    Parameters:
    url (str): The URL of the server endpoint.
    data (dict): The data to send.

    Returns:
    dict: The server's response.
    """
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()