import json

from .utils import post_request, get_request, delete_request, patch_request

with open("../secrets/config.json") as f:
    config = json.load(f)
    API_KEY = config["api_key"]
    BASE_URL = config["base_url"]

def list():
    url = f"{BASE_URL}/api/collection"
    return get_request(url)

def create(collection_data):
    url = f"{BASE_URL}/api/collection"
    return post_request(url, collection_data)

def update(collection_data):
    url = f"{BASE_URL}/api/collection"
    return patch_request(url, collection_data)

def delete(collection_id):
    url = f"{BASE_URL}/api/collection/{collection_id}"
    return delete_request(url)

def get(collection_id):
    url = f"{BASE_URL}/api/collection/{collection_id}"
    return get_request(url)

def search(search_data):
    url = f"{BASE_URL}/api/collection/search"
    return post_request(url)

