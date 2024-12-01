import tensorflow as tf
from google.cloud import storage

BUCKET_NAME = "models-storage-bucket"
MODEL_PATH = "model.h5"
LOCAL_MODEL_PATH = "/tmp/model.h5"

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob(MODEL_PATH)
blob.download_to_filename(LOCAL_MODEL_PATH)

try:
    model = tf.keras.models.load_model(LOCAL_MODEL_PATH)
    print("Model loaded successfully.")
except OSError as e:
    print(f"Error loading model: {e}")
