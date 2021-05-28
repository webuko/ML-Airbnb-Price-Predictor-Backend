import json
import requests
import pickle
from collections import OrderedDict


# url for accessing price prediction micro service
PRICE_PREDICTOR_URL = "http://tensorflow-serving:8501/v1/models/price_predictor:predict"
# model (and version) to use
PRICE_PREDICTOR_ENCODER_LOCATION = "encoders/airbnb_price_net/1/"

"""
This ordered dict stores all necessary fields for the price prediction.
Note that it's an ordered dict and the order corresponds to the order of the feature list that must be provided to
the prediction model.
"""
NECESSARY_FIELDS = OrderedDict([
    ('bathrooms', ('num', [0, 100])),
    ('bedrooms', ('num', [0, 100])),
    ('accommodates', ('num', [0, 100])),
    ('guests_included', ('num', [0, 100])),
    ('gym', ('binary', [True, False])),
    ('ac', ('binary', [True, False])),
    ('elevator', ('binary', [True, False])),
    ('neighbourhood', ('encode', None)),
    ('property_type', ('encode', None)),
    ('room_type', ('encode', None))
])


def load_encoder_and_transform(encoder, val):
    """Loads an encoder and then encodes the given value.

    :param encoder: the name of the decoder that should be used
    :type: string
    :param val: the value that should be encoded
    :type: string

    :returns: a dictionary containing the encoded value (error and error msg in case of an error)
    :rtype: dict
    """

    try:
        encoder = pickle.load(open(f'{PRICE_PREDICTOR_ENCODER_LOCATION}{encoder}_encoder.pickle', 'rb'))
    except FileNotFoundError:
        return {'error': {'code': 500, 'msg': 'Internal server error. Please try again later'}}

    if val not in encoder.classes_:
        return {'error': {'code': 400, 'msg': f'{val} does not exist'}}

    return {'encoded': encoder.transform([val]).tolist()[0]}


def encoder_classes(encoder):
    """Get possible encoder values for a given encoder.

    :param encoder: the name of the decoder that should be used
    :type: string

    :returns: a list containing the possible encoder values
    :rtype: list
    """

    try:
        encoder = pickle.load(open(f'{PRICE_PREDICTOR_ENCODER_LOCATION}{encoder}_encoder.pickle', 'rb'))
    except FileNotFoundError:
        return False
    return encoder.classes_.tolist()


def validate_prediction_request(request):
    """Validate and process a price prediction request.
    
    :param request: the request object sent by the user
    :type: flask.request

    :returns: a dictionary containing the processed request (error and error msg in case of an error)
    :rtype: dict
    """

    features = []

    if not request.json or not isinstance(request.json, dict):
        return {'error': {'code': 400, 'msg': 'Request data must be transmitted as JSON object'}}

    for field, (t, vals) in NECESSARY_FIELDS.items():
        if request.json.get(field) is None:
            return {'error': {'code': 400, 'msg': 'Make sure all required fields are submitted'}}

        el = request.json.get(field)

        if t == 'num':
            if not isinstance(el, int) or el < vals[0] or el > vals[1]:
                return {'error': {'code': 400, 'msg': f'unallowed value for {field}'}}
            features.append(el)

        elif t == 'binary':
            if not isinstance(el, bool):
                return {'error': {'code': 400, 'msg': f'unallowed value for {field}'}}
            features.append(int(el))
            
        else:
            encoded = load_encoder_and_transform(field, el)
            if 'error' in encoded:
                return encoded
            features += encoded['encoded']

    return {'instances': [features]}


def get_prediction(instances):
    """Send a processed request to the prediction microservice.
    
    :param instances: a list containing the features in the needed format for the prediction model
    :type: list

    :returns: the prediction
    :rtype: str
    """
    
    request_data = json.dumps(instances)

    request = requests.post(PRICE_PREDICTOR_URL, request_data)

    if request.status_code == 200:
        return str(json.loads(request.text)['predictions'][0][0])
    else:
        return str(request.text)


def allowed_prediction_features():
    """Send a processed request to the prediction microservice.

    :returns: the necessary fields along with the type and allowed values
    :rtype: dict
    """
    
    features = {}
    for field, (t, vals) in NECESSARY_FIELDS.items():
        if t != 'encode':
            features[field] = {'type': t, 'values': vals}
        else:
            encoder_vals = encoder_classes(field)
            features[field] = {'type': 'string', 'values': encoder_vals}
    return features
