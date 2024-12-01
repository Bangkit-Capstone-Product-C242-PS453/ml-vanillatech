import base64
import json
import io
import logging
from google.cloud import pubsub_v1
from services.predict import predict_image

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PROJECT_ID = "capstone-c242-ps453"
SUBSCRIPTION_NAME = "process-image-sub"
PUBLISH_TOPIC_NAME = "result-image"

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)
publish_topic_path = publisher.topic_path(PROJECT_ID, PUBLISH_TOPIC_NAME)

# Callback function to handle incoming Pub/Sub messages
def callback(message: pubsub_v1.subscriber.message.Message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        image_data = base64.b64decode(data['image'])
        timestamp = data['timestamp']

        logger.debug(f"Received image with timestamp: {timestamp}")

        # Process the image and get predictions
        image_stream = io.BytesIO(image_data)
        predictions = predict_image(image_stream)

        # Prepare the result to be published
        result = {
            "id_process": message.message_id,
            "result": predictions,
            "timestamp": timestamp
        }

        # Publish the result to another Pub/Sub topic
        publisher.publish(publish_topic_path, json.dumps(result).encode("utf-8"))
        logger.debug(f"Published result: {result}")

        # Acknowledge the message
        message.ack()
        logger.debug("Message acknowledged")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        message.nack()
        logger.debug("Message not acknowledged due to error")

# Cloud Function that listens to Pub/Sub messages
def listen_to_pubsub(event, context):
    """Triggered by a Pub/Sub message."""
    # Subscribe to the Pub/Sub subscription to start listening for messages
    subscriber.subscribe(subscription_path, callback=callback)
    logger.info(f"Listening for messages on {subscription_path}...")
    return "Listening for messages..."
