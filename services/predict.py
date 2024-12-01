from models.model import model
from utils.preprocess import preprocess_image

CLASS_NAMES = ['Akar Busuk', 'Busuk Batang', 'Busuk Daun', 'Hawar Daun dan Bunga', 'Powder Mildew', 'Sehat']

def predict_image(image_stream):
    """
    Prediksi gambar berdasarkan model ML.
    :param image_stream: Stream file gambar (BytesIO).
    :return: Dictionary berisi confidence untuk setiap kelas.
    """
    processed_image = preprocess_image(image_stream)
    predictions = model.predict(processed_image)
    probabilities = predictions[0]  

    return {CLASS_NAMES[i]: float(probabilities[i] * 100) for i in range(len(CLASS_NAMES))}
