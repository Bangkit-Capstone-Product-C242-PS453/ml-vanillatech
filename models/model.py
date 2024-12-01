import tensorflow as tf

MODEL_PATH = "models/model.h5"
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully.")
except OSError as e:
    print(f"Error loading model: {e}")

