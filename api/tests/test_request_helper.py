import sys
from pathlib import Path

from flask import Flask, request

parent = Path(__file__).resolve().parents[1]
sys.path.append(str(parent) + '/code/flaskr/')
import request_helper

import pytest
import json


@pytest.fixture
def flask_app():
    app = Flask(__name__)
    app.testing = True
    return app


def test_project_listings_get(flask_app):
    """Tests whether a get request for retrieving all listings will return default projection and filter keys for db query."""

    with flask_app.test_request_context():
        projected_request = request_helper.project_listings(request)
        assert ('keys_filter' in projected_request and 'keys_projection' in projected_request)

def test_project_listings_fields_param_missing(flask_app):
    """Tests whether a post request for retrieving all listings with missing fields param will return correct error."""

    data = {
        'test': 0
    }
    with flask_app.test_request_context(json=data, method='POST'):
        projected_request = request_helper.project_listings(request)
        assert ('error' in projected_request 
        and projected_request['error']['msg'] == 'fields parameter missing')

def test_project_listings_force_fields_wrong_type(flask_app):
    """Tests whether a post request for retrieving all listings with wrong force_fields param type will return correct error."""

    data = {
        'fields': ['price'],
        'force_fields': 'test'
    }
    with flask_app.test_request_context(json=data, method='POST'):
        projected_request = request_helper.project_listings(request)
        assert ('error' in projected_request 
        and projected_request['error']['msg'] == 'force_field parameter must be provided as bool')

def test_project_listings_fields_wrong_type(flask_app):
    """Tests whether a post request for retrieving all listings with missing fields param will return correct error."""

    data = {
        'fields': 'test'
    }
    with flask_app.test_request_context(json=data, method='POST'):
        projected_request = request_helper.project_listings(request)
        assert ('error' in projected_request 
        and projected_request['error']['msg'] == 'Request data must be provided as array of keys')

def test_project_listings_valid_request_fields(flask_app):
    """Tests whether a post request for retrieving all listings with with correct fields param is validated."""

    data = {
        'fields': ['price']
    }
    with flask_app.test_request_context(json=data, method='POST'):
        projected_request = request_helper.project_listings(request)
        assert ('keys_filter' in projected_request and 'keys_projection' in projected_request)

def test_project_listings_valid_request_fields_and_force_fields(flask_app):
    """Tests whether a post request for retrieving all listings with with correct fields param is validated."""

    data = {
        'fields': ['price'],
        'force_fields': True
    }
    with flask_app.test_request_context(json=data, method='POST'):
        projected_request = request_helper.project_listings(request)
        assert ('keys_filter' in projected_request and 'keys_projection' in projected_request)