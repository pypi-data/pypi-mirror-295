import base64
import json
from google.cloud import pubsub_v1, secretmanager
import requests
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Capture DEBUG, INFO, WARNING, ERROR, CRITICAL

def fetch_gcp_project_id() -> str:
    metadata_server_url = "http://metadata/computeMetadata/v1/project/project-id"
    headers = {"Metadata-Flavor": "Google"}
    project_id = requests.get(metadata_server_url, headers=headers).text
    return project_id

def fetch_gcp_secret(secret_name: str) -> str:
    # Fetch Project ID from Metadata Server
    project_id = fetch_gcp_project_id()
    
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    secret_version = 'latest'
    name = f"projects/{project_id}/secrets/{secret_name}/versions/{secret_version}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})
    secret_string = response.payload.data.decode("UTF-8")
    return secret_string

# Get pipeline_id from the message
def get_pipeline_id(event: dict) -> str:
    if 'data' in event:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        pubsub_message = json.loads(pubsub_message)
        if 'pipeline_id' in pubsub_message:
            return pubsub_message['pipeline_id']
        else:
            logger.error("Pipeline ID is missing in the message")
            return ""
    else:
        logger.error("Data is missing in the event")
        return ""

def publish_to_pubsub(topic_name : str, data : dict) -> bool:
    """Publishes a message to a Google Cloud Pub/Sub topic."""
    # Fetch Project ID from Metadata Server
    project_id = fetch_gcp_project_id()
    # Publish the message to Pub/Sub
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_name)
        data = json.dumps(data).encode("utf-8")
        future = publisher.publish(topic_path, data)
        logger.debug(f"Publishing completed with message ID: {future.result()}")
        logger.debug(f"Published message to topic: {topic_name} and project_id: {project_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to publish message: {str(e)}")
        return False
    
def openAI_request(api_key: str, role: str, request: str) -> dict:
    client = OpenAI(api_key=api_key)
    try:
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": request},
            ])
    except Exception as e:
        logger.error(f"Failed to get completion from OpenAI: {str(e)}")
        return None
    return completion

def load_valid_json(string) -> dict:
    try:
        loaded_json = json.loads(string)
        return loaded_json
    except Exception as e:
        logger.error(f"JSON validation failed: {str(e)}, string: {string}")
        return None
    
def load_current_pipeline_data(pipeline_id: str):
    api_url = fetch_gcp_secret('adaptive-pipeline-persistence-layer-url')
    api_key = fetch_gcp_secret('adaptive-pipeline-API-token')

    if not api_url:
        logger.error("Failed to fetch the API URL")
        return None
    headers = {
            "Authorization": api_key
        }
    try:
        response = requests.get(f"{api_url}/read/{pipeline_id}", headers=headers)
        if response.status_code != 200:
            logger.error(f"Failed to fetch the pipeline data. Response: {response.text}")
            return None
        pipeline_data = response.json()
        return pipeline_data
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return None   

def save_current_pipeline_data(pipeline_data: dict) -> bool:
    api_url = fetch_gcp_secret('adaptive-pipeline-persistence-layer-url')
    api_key = fetch_gcp_secret('adaptive-pipeline-API-token')
    if not api_url:
        logger.error("Failed to fetch the API URL")
        return None
    headers = {
            "Authorization": api_key
        }
    try:
        response = requests.put(f"{api_url}/update/{pipeline_data['pipeline_id']}", json=pipeline_data, headers=headers)
        if response.status_code != 200:
            logger.error(f"Failed to update the pipeline status. Response: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return False
    