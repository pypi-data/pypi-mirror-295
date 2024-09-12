import json

from .utils import post_request, get_request, delete_request, patch_request

with open("../secrets/config.json") as f:
    config = json.load(f)
    API_KEY = config["api_key"]
    BASE_URL = config["base_url"]

def list():
    url = f"{BASE_URL}/api/role"
    return get_request(url)

def create(role_data):
    url = f"{BASE_URL}/api/role"
    return post_request(url, role_data)

def update(role_data):
    url = f"{BASE_URL}/api/role"
    return patch_request(url, role_data)

def delete(role_id):
    url = f"{BASE_URL}/api/role/{role_id}"
    return delete_request(url)

def get(role_id):
    url = f"{BASE_URL}/api/role/{role_id}"
    return get_request(url)