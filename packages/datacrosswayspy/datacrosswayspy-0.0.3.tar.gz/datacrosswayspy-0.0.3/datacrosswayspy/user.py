import json

from .utils import post_request, get_request, delete_request, patch_request

with open("../secrets/config.json") as f:
    config = json.load(f)
    API_KEY = config["api_key"]
    BASE_URL = config["base_url"]

def i():
    url = f"{BASE_URL}/api/user/i"
    return get_request(url)
    
def list():
    url = f"{BASE_URL}/api/user"
    return get_request(url)
    
def get(user_id):
    url = f"{BASE_URL}/api/user/{user_id}"
    return get_request(url)
    
def files():
    url = f"{BASE_URL}/api/user/file"
    return get_request(url)

def access_keys():
    url = f"{BASE_URL}/api/user/accesskey"
    return get_request(url)
    
def create_key(exp_time):
    url = f"{BASE_URL}/api/user/accesskey/{exp_time}"
    return post_request(url)

def create(user_information):
    url = f"{BASE_URL}/api/user"
    return post_request(url, data=user_information)

def create_list(user_information_list):
    url = f"{BASE_URL}/api/user/bulk"
    return post_request(url, data=user_information_list)

def update(user_information):
    url = f"{BASE_URL}/api/user"
    return patch_request(url, data=user_information)

def delete(user_id):
    url = f"{BASE_URL}/api/user/{user_id}"
    return delete_request(url)

def logs(user_id, offset=0, limit=20):
    endpoint_url = f"{BASE_URL}/api/user/log/{user_id}"
    params = {
        'offset': offset,
        'limit': limit
    }
    return get_request(endpoint_url, params=params)
