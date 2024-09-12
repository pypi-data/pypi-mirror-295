import requests
import json

with open("../secrets/config.json") as f:
    config = json.load(f)
    API_KEY = config["api_key"]
    BASE_URL = config["base_url"]

def get_request(url, params=None):
    headers = {
        "x-api-key": API_KEY
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Could not retrieve information. Status code: {response.status_code}. Response: {response.text}")
        return {}

def post_request(url, data={}):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to post data. {response.text}")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=4))
        except json.JSONDecodeError:
            print(response.text)
        return {}

def patch_request(url, data={}):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to update data. {response.text}")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=4))
        except json.JSONDecodeError:
            print(response.text)
        return {}

def delete_request(url):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to post data. {response.text}")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=4))
        except json.JSONDecodeError:
            print(response.text)