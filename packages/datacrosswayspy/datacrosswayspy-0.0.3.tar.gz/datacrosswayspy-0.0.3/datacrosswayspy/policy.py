import json

from .utils import post_request, get_request, delete_request

with open("../secrets/config.json") as f:
    config = json.load(f)
    API_KEY = config["api_key"]
    BASE_URL = config["base_url"]

def list():
    url = f"{BASE_URL}/api/policy"
    return get_request(url)

def create(policy_data):
    url = f"{BASE_URL}/api/policy"
    return post_request(url, policy_data)

def delete(policy_id):
    url = f"{BASE_URL}/api/policy/{policy_id}"
    return delete_request(url)

def get(policy_id):
    url = f"{BASE_URL}/api/policy/{policy_id}"
    return get_request(url)