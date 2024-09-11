import os
import requests
import gzip
import logging
from google.cloud import storage
from .config import OUTPUT_METHOD, HTTP_ENDPOINT, TLS_CERT_PATH, TLS_KEY_PATH, AUTH_METHOD, AUTH_TOKEN, API_KEY, OUTPUT_DIR

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_file(bucket_name, file_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        file = bucket.blob(file_name)
        return file.download_as_bytes()
    except Exception as e:
        logging.error(f"Failed to download file: gs://{bucket_name}/{file_name}, error: {e}")
        raise

def process_log_file(bucket_name, file_name):
    compressed_content = download_file(bucket_name, file_name)
    decompressed_content = gzip.decompress(compressed_content).decode('utf-8')
    logs = decompressed_content.split('\n')

    if OUTPUT_METHOD == 'files':
        # Ensure OUTPUT_DIR ends with a slash
        normalized_output_dir_path = OUTPUT_DIR if OUTPUT_DIR.endswith('/') else OUTPUT_DIR + '/'
        # Strip the leading slash from file_name
        file_name = file_name.lstrip('/')
        
        # Construct the local path based on the file name
        local_path = os.path.join(normalized_output_dir_path, file_name)
        local_dir = os.path.dirname(local_path)

        # Create directories if they do not exist
        os.makedirs(local_dir, exist_ok=True)
        with gzip.open(local_path, 'at') as file:
            for log in logs:
                if log.strip():
                    write_log_to_file(log, file)
    else:
        for log in logs:
            if log.strip():
                send_log_to_http(log)

def send_log_to_http(log):
    try:
        headers = {'Content-Type': 'application/json'}
        cert = None

        if TLS_CERT_PATH and TLS_KEY_PATH:
            cert = (TLS_CERT_PATH, TLS_KEY_PATH)

        if AUTH_METHOD == 'token' and AUTH_TOKEN:
            headers['Authorization'] = f'Bearer {AUTH_TOKEN}'
        elif AUTH_METHOD == 'api_key' and API_KEY:
            headers['X-API-Key'] = API_KEY

        response = requests.post(HTTP_ENDPOINT, data=log, headers=headers, cert=cert)
        response.raise_for_status()
        logging.info(f"Log forwarded successfully to HTTP endpoint: {log}")
    except Exception as e:
        logging.error(f"Failed to forward log to HTTP endpoint, error: {e}")

def write_log_to_file(log, file):
    if log.strip():  # Ensure that empty or whitespace-only lines are not written
        try:
            file.write(log + '\n')
            logging.info(f"Log written successfully to file: {log}")
        except Exception as e:
            logging.error(f"Failed to write log to file, error: {e}")
