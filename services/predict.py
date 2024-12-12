from models.model import model
from utils.preprocess import preprocess_image

def prediction(image_stream):
    classes = ['Akar Busuk', 'Busuk Batang', 'Busuk Daun', 'Hawar Daun dan Bunga', 'Powdery Mildew', 'Sehat']

    processed_image = preprocess_image(image_stream)
    predictions = model.predict(processed_image)
    probabilities = predictions[0]  

    return {classes[i]: float(probabilities[i] * 100) for i in range(len(classes))}