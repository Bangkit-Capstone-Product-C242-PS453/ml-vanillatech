import tensorflow as tf
from io import BytesIO

def preprocess_image(image_stream):
    """
    Preprocessing gambar sesuai spesifikasi.
    :param image_stream: Stream file gambar (BytesIO).
    :return: Tensor siap digunakan model.
    """
    image_bytes = image_stream.read()
    img = tf.image.decode_image(image_bytes, channels=3)
    img = tf.image.resize(img, [256, 256])
    img = tf.expand_dims(img, 0)  # Menambahkan batch dimension
    return img
