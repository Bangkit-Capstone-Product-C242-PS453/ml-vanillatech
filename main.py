import base64
import json
import io
import logging
import asyncio
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import RedirectResponse
from google.cloud import pubsub_v1
from services.predict import predict_image
from models.model import reload_model

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

@app.post("/reload")
async def reload_model_endpoint():
    try:
        message = reload_model()
        logger.info(message)
        return {"message": message}
    except Exception as e:
        logger.error(f"Error reloading model: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error reloading model: {str(e)}")

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

def callback(message: pubsub_v1.subscriber.message.Message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        image_data = base64.b64decode(data['image'])
        timestamp = data['timestamp']

        logger.debug(f"Received image with timestamp: {timestamp}")

        image_stream = io.BytesIO(image_data)
        try:
            predictions = predict_image(image_stream)
        except Exception as e:
            message.nack()

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
        message.nack()

async def listen_to_pubsub():
    subscriber.subscribe(subscription_path, callback=callback)
    logger.info(f"Listening for messages on {subscription_path}...")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(listen_to_pubsub())