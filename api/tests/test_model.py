import sys
from pathlib import Path

from flask import Flask, request

parent = Path(__file__).resolve().parents[1]
sys.path.append(str(parent) + '/code/flaskr/')
import model

model.PRICE_PREDICTOR_ENCODER_LOCATION = str(parent) + '/code/encoders/airbnb_price_net/1/'

import random
import pytest


"""Contains tests regarding the encoders that are used for some features needed in price prediction. The block just 
below tests whether all necessary encoders can be loaded."""

def test_neighbourhood_encoder_available():
    assert model.encoder_classes('neighbourhood') is not False


def test_property_type_encoder_available():
    assert model.encoder_classes('property_type') is not False


def test_room_type_encoder_available():
    assert model.encoder_classes('room_type') is not False


"""Following tests should make sure that values are correctly encoded and, in the case of an invalid value, 
no encoding is done."""

def test_neighbourhood_valid_example():
    """
    Tests to make sure that values are correctly encoded and, in the case of an invalid value, no encoding is done.
    """
    example = model.encoder_classes('neighbourhood')[0]
    assert 'encoded' in model.load_encoder_and_transform('neighbourhood', example)


def test_neighbourhood_invalid_example():
    assert 'error' in model.load_encoder_and_transform('neighbourhood', 'something')


def test_property_type_valid_example():
    example = model.encoder_classes('property_type')[0]
    assert 'encoded' in model.load_encoder_and_transform('property_type', example)


def test_property_type_invalid_example():
    assert 'error' in model.load_encoder_and_transform('property_type', 'something')


def test_room_type_valid_example():
    example = model.encoder_classes('room_type')[0]
    assert 'encoded' in model.load_encoder_and_transform('room_type', example)


def test_room_type_invalid_example():
    assert 'error' in model.load_encoder_and_transform('room_type', 'something')


@pytest.fixture
def flask_app():
    app = Flask(__name__)
    app.testing = True
    return app


@pytest.fixture
def valid_model_input():
    data = {}
    for field, (t, vals) in model.NECESSARY_FIELDS.items():
        if t == 'num':
            data[field] = random.randint(vals[0], vals[1])
        elif t == 'binary':
            data[field] = random.randint(0, 1)
        else:
            data[field] = random.choice(model.encoder_classes(field))

    return data

def test_model_input_validation_all_fields_submitted(flask_app, valid_model_input):
    with flask_app.test_request_context(data=valid_model_input):
        validated = model.validate_prediction_request(request)
        print(validated)
        assert ('error' in validated and validated['error'][
            'msg'] == 'Make sure all required fields are submitted') is not True

def test_model_input_validation_valid_response(flask_app, valid_model_input):
    with flask_app.test_request_context(data=valid_model_input):
        validated = model.validate_prediction_request(request)
        assert 'instances' in validated

def test_get_prediction(response_mock):
    expected_response = '{\n' \
                        '   \"predictions\": [\n' \
                        '       [42],\n' \
                        '       [6]\n' \
                        '   ]\n' \
                        '}'
    with response_mock('POST ' + model.PRICE_PREDICTOR_URL + f' -> 200 :{expected_response}', bypass=False):
        p = model.get_prediction('anything')
        assert p == '42'