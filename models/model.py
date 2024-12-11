import tensorflow as tf
from google.cloud import storage

# LOCAL_MODEL_PATH = "models/model.h5"

BUCKET_NAME = "models-storage-bucket"
MODEL_PATH = "model.h5"
LOCAL_MODEL_PATH = "/tmp/model.h5"

storage_client = storage.Client()

def load_initial_model():
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(MODEL_PATH)
        blob.download_to_filename(LOCAL_MODEL_PATH)
        model = tf.keras.models.load_model(LOCAL_MODEL_PATH)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

model = load_initial_model()

def reload_model():
    global model
    try:
        model = load_initial_model()
        print("Model reloaded successfully.")
        return "Model reloaded successfully."
    except Exception as e:
        print(f"Error reloading model: {e}")
        raise Exception(f"Error reloading model: {e}")
