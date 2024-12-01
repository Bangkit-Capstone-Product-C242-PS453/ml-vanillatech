import base64
import json
import uuid
import io
import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from google.cloud import pubsub_v1
from services.predict import predict_image

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

PROJECT_ID = "capstone-c242-ps453"
SUBSCRIPTION_NAME = "process-image-sub"
PUBLISH_TOPIC_NAME = "result-image"

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)
publish_topic_path = publisher.topic_path(PROJECT_ID, PUBLISH_TOPIC_NAME)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return RedirectResponse(url="/health")

def callback(message: pubsub_v1.subscriber.message.Message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        image_data = base64.b64decode(data['image'])
        timestamp = data['timestamp']

        logger.debug(f"Received image with timestamp: {timestamp}")

        image_stream = io.BytesIO(image_data)
        predictions = predict_image(image_stream)

        result = {
            "id_process": message.message_id,
            "result": predictions,
            "timestamp": timestamp
        }

        publisher.publish(publish_topic_path, json.dumps(result).encode("utf-8"))
        logger.debug(f"Published result: {result}")

        message.ack()
        logger.debug("Message acknowledged")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        message.nack()
        logger.debug("Message not acknowledged due to error")

def listen_to_pubsub():
    subscriber.subscribe(subscription_path, callback=callback)
    logger.info(f"Listening for messages on {subscription_path}...")

if __name__ == "__main__":
    import threading
    threading.Thread(target=listen_to_pubsub, daemon=True).start()

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
