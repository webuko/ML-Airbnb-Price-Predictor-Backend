import tensorflow as tf
from tensorflow import keras
import json
import requests
import pickle
import sklearn
from collections import OrderedDict


PRICE_PREDICTOR_URL = 'http://tensorflow-serving:8501/v1/models/price_predictor:predict'
PRICE_PREDICTOR_ENCODER_LOCATION = 'encoders/airbnb_price_net/1/'


def validate_prediction_request(request):
    '''
    This function validates the post data sent for a price prediction request.
    The function returns a dict.
    '''

    features = []

    error_msg = 'Make sure all the fields are properly submitted'
    
    # make sure all the necessary attributes were sent
    # the order of the list corresponds to the order that is required by the model to work properly
    necessary_fields = OrderedDict([
        ('bathrooms', 'num'),
        ('bedrooms', 'num'),
        ('accommodates', 'num'),
        ('guests_included', 'num'),
        ('gym', 'binary'),
        ('ac', 'binary'),
        ('elevator', 'binary'),
        ('neighbourhood', 'encode'),
        ('property_type', 'encode'),
        ('room_type', 'encode')

    ])

    for field, t in necessary_fields.items():
        if not request.form.get(field):
            return {'error': error_msg}
        
        el = request.form.get(field)

        if t == 'num':
            if not el.isdigit():
                return {'error': error_msg}
            features.append(float(el))

        elif t == 'binary':
            if not el.isdigit() or int(el) not in [0, 1]:
                return {'error': error_msg}
            features.append(int(el))
        else:
            encoder = pickle.load(open(f'{PRICE_PREDICTOR_ENCODER_LOCATION}{field}_encoder.pickle', 'rb'))
            try:
                features += encoder.transform([el]).tolist()[0]
                if field == 'room_type':
                    return encoder.transform([el]).tolist()[0]
            except:
                return {'error': error_msg}

    return {'instance': features}


def get_prediction(instances):
    # format correctly
    request_data = json.dumps({'instances': [[0]*182]})

    request = requests.post(PRICE_PREDICTOR_URL, request_data)

    if request.status_code == 200:
        return str(json.loads(request.text)['predictions'][0][0])
    else:
        return False
