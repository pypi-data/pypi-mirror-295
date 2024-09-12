import json
import os
import requests
import tqdm
import concurrent.futures
import builtins

from .utils import post_request, get_request, delete_request, patch_request

with open("../secrets/config.json") as f:
    config = json.load(f)
    API_KEY = config["api_key"]
    BASE_URL = config["base_url"]

def list(offset=None, limit=None):
    url = f"{BASE_URL}/api/file"
    params = {}
    if offset is not None:
        params['offset'] = offset
    if limit is not None:
        params['limit'] = limit
    return get_request(url, params=params)

def create(file_data):
    url = f"{BASE_URL}/api/file"
    return post_request(url, file_data)

def update(file_data):
    url = f"{BASE_URL}/api/file"
    return patch_request(url, file_data)

def delete(file_id):
    url = f"{BASE_URL}/api/file/{file_id}"
    return delete_request(url)

def get(file_id):
    url = f"{BASE_URL}/api/file/{file_id}"
    return get_request(url)

def upload(file_path, meta=None, progress=True):
    if type(file_path) is builtins.list:
        if meta is None:
            meta = [None] * len(file_path)
        elif not type(meta) is builtins.list:
            raise ValueError("If file_path is a list, meta should also be a list or None")
        elif len(meta) != len(file_path):
            raise ValueError("Length of meta list must match length of file_path list")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(upload_single, fp, meta=m, progress=progress)
                       for fp, m in zip(file_path, meta)]
            results = []
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
            return results
    else:
        return upload_single(file_path, meta=meta, progress=progress)

def upload_single(file_path, meta=None, progress=True):
    url = f"{BASE_URL}/api/file/upload"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    if file_size > 5*1024*1024:
        res = upload_large_file(file_path, BASE_URL, progress=progress)
    else:
        data = {
            "filename": filename,
            "size": file_size
        }
        response = post_request(url, data)
        upload_file_to_signed_url(file_path, response)
        res = {"name": response["file"]["display_name"] ,"id": response["file"]["id"]}

    if meta:
        update({"id": res["id"], "meta": meta})
    return res

def upload_file_to_signed_url(file_path, signed_url_data):
    # Extract the URL and fields from the signed URL data
    url = signed_url_data['url']['url']
    fields = signed_url_data['url']['fields']

    # Prepare the files dictionary
    files = {'file': open(file_path, 'rb')}

    # Prepare the form data
    data = {**fields}

    try:
        # Make the POST request to upload the file
        response = requests.post(url, data=data, files=files)

        # Check if the upload was successful
        if response.status_code == 204:
            return True
        else:
            print(f"File upload failed. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"An error occurred during file upload: {str(e)}")
        return False
    finally:
        # Ensure the file is closed
        files['file'].close()

def upload_large_file(file_path, base_url, chunk_size=5*1024*1024, progress=True):
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    # Start multipart upload
    headers = {
        "x-api-key": API_KEY
    }
    start_response = requests.post(f"{base_url}/api/file/startmultipart", 
                                   json={"filename": file_name, "size": file_size}, headers=headers)

    if start_response.status_code != 200:
        raise Exception("Failed to start multipart upload")
    
    start_data = start_response.json()
    upload_id = start_data['upload_id']
    uuid = start_data['uuid']
    file_id = start_data['id']
    

    # Upload parts
    parts = []
    with open(file_path, 'rb') as file:
        part_number = 1
        with tqdm.tqdm(total=file_size, unit='B', unit_scale=True, desc="Uploading", disable=not progress) as pbar:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break

                # Get signed URL for this part
                sign_response = requests.post(f"{base_url}/api/file/signmultipart",
                                              json={"filename": f"{uuid}/{file_name}", 
                                                    "upload_id": upload_id, 
                                                    "part_number": part_number}, headers=headers)
                if sign_response.status_code != 200:
                    raise Exception(f"Failed to get signed URL for part {part_number}")

                signed_url = sign_response.json()['url']

                # Upload the part
                upload_response = requests.put(signed_url, data=chunk)
                if upload_response.status_code != 200:
                    raise Exception(f"Failed to upload part {part_number}")

                etag = upload_response.headers['ETag']
                parts.append({"PartNumber": part_number, "ETag": etag})
                part_number += 1

                # Update progress bar
                pbar.update(len(chunk))

    # Complete multipart upload
    complete_response = requests.post(f"{base_url}/api/file/completemultipart",
                                      json={"filename": f"{uuid}/{file_name}", 
                                            "upload_id": upload_id, 
                                            "parts": parts}, headers=headers)
    if complete_response.status_code != 200:
        raise Exception("Failed to complete multipart upload")
    
    print("completed multipart upload", {"id": file_id, "name": file_name, "size": file_size})
    return {"id": file_id, "name": file_name, "size": file_size}


def download(file_id, path):
    endpoint_url = f"{BASE_URL}/api/file/download/{file_id}"
    response = get_request(endpoint_url)

    if response["message"] == "URL signed":
        signed_url = response["url"]
        
        if signed_url:
            file_response = requests.get(signed_url, stream=True)
            
            if file_response.status_code == 200:
                with open(path, 'wb') as file:
                    for chunk in file_response.iter_content(chunk_size=8192):
                        file.write(chunk)
            else:
                print(f"Failed to download file. Status code: {file_response.status_code}")
        else:
            print("No signed URL received from the endpoint")
    else:
        print(f"Failed to get signed URL. Status code: {response.status_code}")

def search(query="", offset=0, limit=20, file_info=None, owner_id=None, collection_id=None):
    endpoint_url = f"{BASE_URL}/api/file/search"
    payload = {
        "query": query,
        "offset": offset,
        "limit": limit,
        "file_info": file_info,
        "owner_id": owner_id,
        "collection_id": collection_id
    }
    
    try:
        response = post_request(endpoint_url, data=payload)
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def logs(file_id, offset=0, limit=20):
    endpoint_url = f"{BASE_URL}/api/file/log/{file_id}"
    params = {
        'offset': offset,
        'limit': limit
    }
    try:
        return get_request(endpoint_url, params=params)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None