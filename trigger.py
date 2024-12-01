import logging
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

FASTAPI_URL = "https://ml-vanillatech-730442888561.asia-southeast2.run.app/predict-trigger"

def pubsub_trigger(pubsub_message):
    try:
        pubsub_message = pubsub_message.get_json()
        logger.debug(f"Received Pub/Sub message: {pubsub_message}")
        response = requests.post(FASTAPI_URL, json=pubsub_message)
        if response.status_code == 200:
            logger.info(f"Request to FastAPI successful: {response.json()}")
        else:
            logger.error(f"Request to FastAPI failed with status code {response.status_code}: {response.text}")

        return "Prediction Triggered Successfully"
    
    except Exception as e:
        logger.error(f"Error processing Pub/Sub message: {e}")
        return f"Error: {e}", 500