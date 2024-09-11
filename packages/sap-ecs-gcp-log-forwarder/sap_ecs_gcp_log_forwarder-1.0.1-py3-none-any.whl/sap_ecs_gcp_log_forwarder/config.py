import os

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
PUBSUB_SUBSCRIPTION = os.getenv('PUBSUB_SUBSCRIPTION')
TIMEOUT_DURATION = None if os.getenv('TIMEOUT_DURATION') is None else int(os.getenv('TIMEOUT_DURATION')) # Timeout duration in seconds
OUTPUT_METHOD = os.getenv('OUTPUT_METHOD', 'http') # 'http' or 'files'

HTTP_ENDPOINT = os.getenv('HTTP_ENDPOINT')
TLS_CERT_PATH = os.getenv('TLS_CERT_PATH')
TLS_KEY_PATH = os.getenv('TLS_KEY_PATH')
AUTH_METHOD = os.getenv('AUTH_METHOD', 'token') # 'token' or 'api_key'
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
API_KEY = os.getenv('API_KEY')

OUTPUT_DIR = os.getenv('OUTPUT_DIR')