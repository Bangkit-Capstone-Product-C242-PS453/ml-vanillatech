import tensorflow as tf

def preprocess_image(image_stream):
    image_bytes = image_stream.read()
    img = tf.image.decode_image(image_bytes, channels=3)
    img = tf.image.resize(img, [256, 256])
    img = tf.expand_dims(img, 0)  # Menambahkan batch dimension
    return img
