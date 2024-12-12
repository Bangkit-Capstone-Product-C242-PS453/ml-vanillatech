from models.model import model
from utils.preprocess import preprocess_image

CLASSES = [
    'Akar Busuk', 
    'Busuk Batang', 
    'Busuk Daun', 
    'Hawar Daun dan Bunga', 
    'Powdery Mildew', 
    'Sehat'
]

def predict_image(image_stream):
    processed_image = preprocess_image(image_stream)
    predictions = model.predict(processed_image)
    probabilities = predictions[0]  

    return {CLASSES[i]: float(probabilities[i] * 100) for i in range(len(CLASSES))}
