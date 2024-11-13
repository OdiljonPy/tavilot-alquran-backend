import requests


def validate_phone_number(phone_input):
    url = "http://127.0.0.1:8000/api/v1/auth/login/"
    headers = {
        "Content-Type": "application/json",
    }
    phone_number = f'+998{phone_input.value}'
    data = {
        "phone_number": phone_number,
        'password': '1'
    }
    response = requests.post(url=url, json=data, headers=headers)

    if response.status_code == 200:
        print(f'Data send successfully: {response.json()}')
    else:
        print(f"Error: {response.json()}")