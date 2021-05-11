import tensorflow as tf

from tensorflow import keras

def load_model():
    return True

def get_prediction(latitude, longitude):
    model_path = 'model/airbnb_price_net'
    new_net = tf.keras.models.load_model(model_path)
    result = new_net.predict([[0]*179])
    print(result[0][0])
    return result[0][0]
