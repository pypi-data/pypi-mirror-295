import time
import json
import logging
from google.cloud import pubsub_v1
from .config import GOOGLE_APPLICATION_CREDENTIALS, GCP_PROJECT_ID, PUBSUB_SUBSCRIPTION, TIMEOUT_DURATION, OUTPUT_METHOD, HTTP_ENDPOINT, AUTH_METHOD, AUTH_TOKEN, API_KEY, OUTPUT_DIR
from .log_processor import process_log_file

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Variable to track if a message was received
message_received = False

MAX_RETRIES = 5 # Maximum number of retries for a message

def validate_inputs():
    errors = []

    def validate_string(var_name, var_value):
        if not var_value or not isinstance(var_value, str):
            errors.append(f"{var_name} is required and must be a string.")

    validate_string("GOOGLE_APPLICATION_CREDENTIALS", GOOGLE_APPLICATION_CREDENTIALS)
    validate_string("GCP_PROJECT_ID", GCP_PROJECT_ID)
    validate_string("PUBSUB_SUBSCRIPTION", PUBSUB_SUBSCRIPTION)
    validate_string("OUTPUT_METHOD", OUTPUT_METHOD)

    if OUTPUT_METHOD not in ['http', 'files']:
        errors.append("OUTPUT_METHOD must be either 'http' or 'files'.")

    if OUTPUT_METHOD == 'http':
        validate_string("HTTP_ENDPOINT", HTTP_ENDPOINT)
        validate_string("AUTH_METHOD", AUTH_METHOD)
        if AUTH_METHOD not in ['token', 'api_key']:
            errors.append("AUTH_METHOD must be either 'token' or 'api_key' when OUTPUT_METHOD is 'http'.")
        if AUTH_METHOD == 'token':
            validate_string("AUTH_TOKEN", AUTH_TOKEN)
        elif AUTH_METHOD == 'api_key':
            validate_string("API_KEY", API_KEY)
    elif OUTPUT_METHOD == 'files':
        validate_string("OUTPUT_DIR", OUTPUT_DIR)

    if errors:
        raise ValueError("Input validation failed with the following errors:\n" + "\n".join(errors))

def is_relevant_event(file_name):
    """Filter relevant file events based on the file name."""
    # Check that the file name contains "logserv"
    relevant_identifier = 'logserv'
    return relevant_identifier in file_name

def callback(message):
    global message_received
    logging.debug("Received a message")
    message_received = True

    # Read message content
    message_content = None
    try:
        message_content = json.loads(message.data.decode('utf-8'))
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON message: {e}")
        message.ack()
        return

    bucket_name = message_content.get('bucket')
    file_name = message_content.get('name')
    if not bucket_name or not file_name:
        logging.error(f"Missing bucket or file name in message: {message_content}")
        message.ack()
        return
    
    # Check for event type and relevant file name
    event_type = message.attributes.get('eventType')
    if event_type != 'OBJECT_FINALIZE' or not is_relevant_event(file_name):
        logging.debug(f"Irrelevant message: event_type={event_type}, file_name={file_name}. Skipping message.")
        message.ack()
        return

    # Retry logic
    retries = 0
    while retries < MAX_RETRIES:
        try:
            process_log_file(bucket_name, file_name)
            logging.info(f"Processed log file from bucket: {bucket_name}, file: {file_name}")
            message.ack()
            logging.debug("Message acknowledged")
            return
        except Exception as e:
            retries += 1
            logging.error(f"Error processing log file from bucket {bucket_name}, file {file_name}: {e}")
            if retries == MAX_RETRIES:
                logging.error(f"Max retries reached for message: {message.data}")
                message.ack()  # Acknowledge the message after all retries
                return

def consume_pub_sub():
    # Validate inputs before starting the queue consumer
    validate_inputs()

    global message_received

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(GCP_PROJECT_ID, PUBSUB_SUBSCRIPTION)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    logging.info(f"Listening for messages on {subscription_path}...")

    start_time = time.time()

    try:
        while True:
            elapsed_time = time.time() - start_time
            if TIMEOUT_DURATION and elapsed_time > TIMEOUT_DURATION:
                logging.info("Timeout reached. Exiting.")
                streaming_pull_future.cancel()
                break

            if not message_received:
                logging.info("No messages received. Waiting...")
                time.sleep(20)  # Sleep for a while before checking again

            message_received = False  # Reset the flag for the next iteration
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        logging.info("Forwarder stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        streaming_pull_future.cancel()

if __name__ == "__main__":
    consume_pub_sub()
