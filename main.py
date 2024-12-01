import io
import logging
import base64
import os
from fastapi import FastAPI, HTTPException, Body, Header
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
from services.predict import predict_image

load_dotenv()
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return RedirectResponse(url="/health")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/predict")
async def predict(
    image: str = Body(...),
    timestamp: str = Body(...),
    authorization: str = Header(None)
):
    if not authorization or authorization.split(" ")[-1] != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing Bearer token")

    try:
        image_data = base64.b64decode(image)
        buffer = io.BytesIO(image_data)

        predictions = predict_image(buffer)
        return {"predictions": predictions, "timestamp": timestamp}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the image: {str(e)}")
