import base64
import json
import io
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
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

@app.get("/")
async def root():
    return RedirectResponse(url="/health")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        buffer = io.BytesIO(file_content)

        predictions = predict_image(buffer)
        publisher.publish(publish_topic_path, json.dumps(predictions).encode("utf-8"))
        return {"predictions": predictions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the image: {str(e)}")

@app.on_event("startup")
async def start_polling():
    app.add_task(poll_pubsub)

async def poll_pubsub():
    try:
        response = subscriber.pull(subscription=subscription_path, max_messages=10, timeout=10)
        if response.received_messages:
            for msg in response.received_messages:
                process_message(msg)
    except Exception as e:
        logger.error(f"Error polling Pub/Sub: {e}")

def process_message(message):
    try:
        data = json.loads(message.message.data.decode("utf-8"))
        image_data = base64.b64decode(data['image'])
        timestamp = data['timestamp']

        logger.debug(f"Received image with timestamp: {timestamp}")

        image_stream = io.BytesIO(image_data)
        predictions = predict_image(image_stream)

        result = {
            "id_process": message.message.message_id,
            "result": predictions,
            "timestamp": timestamp
        }

        publisher.publish(publish_topic_path, json.dumps(result).encode("utf-8"))
        logger.debug(f"Published result: {result}")

        subscriber.acknowledge(subscription=subscription_path, ack_ids=[message.ack_id])
        logger.debug("Message acknowledged")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
