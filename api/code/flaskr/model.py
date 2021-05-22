import json
import requests
import pickle
from collections import OrderedDict


# url for accessing price prediction micro service
PRICE_PREDICTOR_URL = "http://tensorflow-serving:8501/v1/models/price_predictor:predict"
# model (and version) to use
PRICE_PREDICTOR_ENCODER_LOCATION = "encoders/airbnb_price_net/1/"

# this ordered dict stores all necessary fields for the price prediction
# note that it's an ordered dict and the order corresponds to the order of the feature list that must be provided to the prediction model
NECESSARY_FIELDS = OrderedDict([
        ('bathrooms', ('num', [0, 100])),
        ('bedrooms', ('num', [0, 100])),
        ('accommodates', ('num', [0, 100])),
        ('guests_included', ('num', [0, 100])),
        ('gym', ('binary', [0, 1])),
        ('ac', ('binary', [0, 1])),
        ('elevator', ('binary', [0, 1])),
        ('neighbourhood', ('encode', None)),
        ('property_type', ('encode', None)),
        ('room_type', ('encode', None))
    ])


def load_encoder_and_transform(encoder, val):
    try:
        encoder = pickle.load(open(f'{PRICE_PREDICTOR_ENCODER_LOCATION}{encoder}_encoder.pickle', 'rb'))
    except:
        return {'error': {'code': 500, 'msg': f'Internal server error. Please try again later'}}

    if val not in encoder.classes_:
        return {'error': {'code': 400, 'msg': f'{val} does not exist'}}

    return {'encoded': encoder.transform([val]).tolist()[0]}


def encoder_classes(encoder):
    try:
        encoder = pickle.load(open(f'{PRICE_PREDICTOR_ENCODER_LOCATION}{encoder}_encoder.pickle', 'rb'))
    except:
        return False
    return encoder.classes_


def validate_prediction_request(request):
    '''
    This function validates the post data sent for a price prediction request.
    The function returns a dict.
    '''
    features = []

    for field, (t, vals) in NECESSARY_FIELDS.items():
        if not request.form.get(field):
            return {'error': {'code': 400, 'msg': 'Make sure all required fields are submitted'}}

        el = request.form.get(field)

        if t == 'num':
            if not el.isdigit() or int(el) < vals[0] or int(el) > vals[1]:
                return {'error': {'code': 400, 'msg': f'unallowed value for {field}'}}
            features.append(float(el))

        elif t == 'binary':
            if not el.isdigit() or int(el) not in vals:
                return {'error': {'code': 400, 'msg': f'unallowed value for {field}'}}
            features.append(int(el))
        else:
            encoded = load_encoder_and_transform(field, el)
            if 'error' in encoded:
                return encoded
            features += encoded['encoded']

    return {'instances': [features]}


def get_prediction(instances):
    # format correctly
    request_data = json.dumps(instances)

    request = requests.post(PRICE_PREDICTOR_URL, request_data)

    if request.status_code == 200:
        return str(json.loads(request.text)['predictions'][0][0])
    else:
        return str(request.text)
