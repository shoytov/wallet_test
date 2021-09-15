import os
import random
import threading

import requests
from requests.exceptions import Timeout, TooManyRedirects, RequestException, HTTPError, ConnectionError
from tqdm import tqdm

url = os.environ.get('URL')
headers = {
    'api-key': os.environ.get('API_KEY')
}
progress = tqdm(total=50000)


def make_transactions() -> None:
    for _ in range(1000):
        try:
            response = requests.get(url=f'{url}/balance/100', headers=headers, timeout=3)
        except (Timeout, TooManyRedirects, RequestException, HTTPError, ConnectionError) as e:
            print(f'get request failed: {e}')
        else:
            if response.status_code != 200:
                print(f'GET status code: {response.status_code}')
        
        add_payload = {
            "user_id": 100,
            "currency": "TEST",
            "value": 100,
            "info": {}
        }
        
        try:
            response = requests.post(url=f'{url}/add_to_wallet', json=add_payload, headers=headers, timeout=3)
        except (Timeout, TooManyRedirects, RequestException, HTTPError, ConnectionError) as e:
            print(f'add transaction failed: {e}')
        else:
            if response.status_code != 201 and response.status_code != 400:
                print(f'ADD status code: {response.status_code}')

        subtract_payload = {
            "user_id": 100,
            "currency": "TEST",
            "value": 100,
            "lesson_id": random.randrange(1, 9000000),
            "info": {}
        }
        
        try:
            response = requests.post(
                    url=f'{url}/subtract_from_wallet', json=subtract_payload, headers=headers, timeout=3
            )
        except (Timeout, TooManyRedirects, RequestException, HTTPError, ConnectionError) as e:
            print(f'subtract transaction failed: {e}')
        else:
            if response.status_code != 200 and response.status_code != 400:
                print(f'SUBTRACT status code: {response.status_code}')

        progress.update()
        

if __name__ == '__main__':
    for _ in range(50):
        t = threading.Thread(target=make_transactions, name="WalletTest")
        t.start()
        