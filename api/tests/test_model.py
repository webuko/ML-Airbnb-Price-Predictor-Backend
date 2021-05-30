import sys
from pathlib import Path

from flask import Flask, request

# add path for flaskr module to python's system path (so it can be found)
parent = Path(__file__).resolve().parents[1]
sys.path.append(str(parent) + '/code/flaskr/')
import model

# override constant (constant specified in model corresponds to location inside dockerized application)
model.PRICE_PREDICTOR_ENCODER_LOCATION = str(parent) + '/code/encoders/airbnb_price_net/1/'

import random
import pytest
import json


'''
Contains tests regarding the encoders that are used for some features needed in price prediction. The block just
below tests whether all necessary encoders can be loaded.
'''

def test_neighbourhood_encoder_available():
    """Tests whether the neighbourhood encoder is available."""

    assert model.encoder_classes('neighbourhood') is not False


def test_property_type_encoder_available():
    """Tests whether the property_type encoder is available."""

    assert model.encoder_classes('property_type') is not False


def test_room_type_encoder_available():
    """Tests whether the room_type encoder is available."""
    assert model.encoder_classes('room_type') is not False


'''
Following tests should make sure that values are correctly encoded and, in the case of an invalid value,
no encoding is done.
'''

def test_neighbourhood_valid_example():
    """Tests the encoding of a valid input for the neighbourhood encoder."""

    example = model.encoder_classes('neighbourhood')[0]
    assert 'encoded' in model.load_encoder_and_transform('neighbourhood', example)


def test_neighbourhood_invalid_example():
    """Tests the encoding of an invalid input for the neighbourhood encoder."""

    assert 'error' in model.load_encoder_and_transform('neighbourhood', 'something')


def test_property_type_valid_example():
    """Tests the encoding of a valid input for the property_type encoder."""

    example = model.encoder_classes('property_type')[0]
    assert 'encoded' in model.load_encoder_and_transform('property_type', example)


def test_property_type_invalid_example():
    """Tests the encoding of an invalid input for the property_type encoder."""

    assert 'error' in model.load_encoder_and_transform('property_type', 'something')


def test_room_type_valid_example():
    """Tests the encoding of a valid input for the room_type encoder."""

    example = model.encoder_classes('room_type')[0]
    assert 'encoded' in model.load_encoder_and_transform('room_type', example)


def test_room_type_invalid_example():
    """ Tests the encoding of an invalid input for the room_type encoder."""

    assert 'error' in model.load_encoder_and_transform('room_type', 'something')


@pytest.fixture
def flask_app():
    """ Returns a flask application instance for testing purposes."""

    app = Flask(__name__)
    app.testing = True
    return app


@pytest.fixture
def valid_model_input():
    """ Returns a valid model input (i.e. for the price prediction model)."""

    data = {}
    for field, (t, vals) in model.NECESSARY_FIELDS.items():
        if t == 'num':
            data[field] = random.randint(vals[0], vals[1])
        elif t == 'binary':
            data[field] = random.choice([True, False])
        else:
            data[field] = random.choice(model.encoder_classes(field))

    return data

def test_model_input_no_json_sent(flask_app):
    with flask_app.test_request_context(method='POST'):
        validated = model.validate_prediction_request(request)
        assert ('error' in validated and validated['error'][
            'msg'] == 'Request data must be transmitted as JSON object')

def test_model_input_validation_all_fields_submitted(flask_app, valid_model_input):
    """Tests the validation for a prediction request with all required fields submitted."""

    with flask_app.test_request_context(method='POST', json=valid_model_input):
        validated = model.validate_prediction_request(request)
        assert ('error' in validated and validated['error'][
            'msg'] == 'Make sure all required fields are submitted') is not True

def test_model_input_validation_valid_response(flask_app, valid_model_input):
    """Tests the validation for a prediction request with valid request data."""

    with flask_app.test_request_context(method='POST', json=valid_model_input):
        validated = model.validate_prediction_request(request)
        assert 'instances' in validated

def test_model_input_validation_binary_field_not_bool(flask_app, valid_model_input):
    # replace correct value for binary field
    valid_model_input['gym'] = json.dumps('test')
    with flask_app.test_request_context(method='POST', json=valid_model_input):
        validated = model.validate_prediction_request(request)
        assert ('error' in validated and validated['error'][
            'msg'] == 'unallowed value for gym')

def test_get_prediction(response_mock):
    """Tests the correct return value from a valid price prediction request."""

    expected_response = '{\n' \
                        '   \"predictions\": [\n' \
                        '       [42],\n' \
                        '       [6]\n' \
                        '   ]\n' \
                        '}'
    with response_mock('POST ' + model.PRICE_PREDICTOR_URL + f' -> 200 :{expected_response}', bypass=False):
        p = model.get_prediction('anything')
        assert p == '42'
