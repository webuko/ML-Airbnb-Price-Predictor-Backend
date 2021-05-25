from flask import Blueprint, request, abort, make_response
from flask_cors import CORS, cross_origin
from flaskr.model import get_prediction, validate_prediction_request, allowed_prediction_features
from flaskr.request_helper import filter_listings
from flaskr.db import mongo

from json import dumps as json_dumps
from bson.json_util import dumps as bson_dumps


api_bp = Blueprint('api', __name__)

# enable cors compatibility
CORS(api_bp)

@api_bp.route('/api/allListings', methods=['GET', 'POST'])
@cross_origin(origins='*', methods=['GET', 'POST'])
def all_listings():
    keys_filter, keys_projection = filter_listings(request)
    json_data = bson_dumps(mongo.db.listings.find(keys_filter, keys_projection))
    response = make_response(json_data, 200)
    response.headers['Content-type'] = 'application/json'

    return response


@api_bp.route('/api/filterListings', methods=['POST'])
@cross_origin(origins='*', methods=['POST'])
def filtered_listings():
    abort_msg = 'filter criteria is not correctly provided'
    keys_filter = {}

    allowed_criteria = {
        'price': 'num',
        'bedrooms': 'num',
        'bathrooms': 'num',
        'accommodates': 'num',
        'property_type': 'str',
        'room_type': 'str',
        'neighbourhood': 'str'
    }

    if not request.json or not isinstance(request.json, dict):
        abort(400, 'Request data must be transmitted as JSON object')

    if not 'criteria' in request.json:
        abort(400, 'criteria parameter missing')

    for criteria, t in allowed_criteria.items():
        el = request.json['criteria'].get(criteria, None)
        if not el:
            continue

        if t == 'num':
            if not isinstance(el, list) or \
                    len(el) != 2 or \
                    (not str(el[0]).isdigit() or not str(el[1]).isdigit()):
                abort(400, abort_msg)
            keys_filter[criteria] = {'$gte': el[0], '$lte': el[1]}
        else:
            if not isinstance(el, list) or \
                    len([e for e in el if str(e).isdigit()]) > 0:
                abort(400, abort_msg)
            keys_filter[criteria] = {'$in': el}

    force_GET = request.json.get('fields') is None
    _, keys_projection = filter_listings(request, force_GET)

    json_data = bson_dumps(mongo.db.listings.find(keys_filter, keys_projection))

    response = make_response(json_data, 200)
    response.headers['Content-type'] = 'application/json'

    return response


@api_bp.route('/api/pricePrediction', methods=['POST'])
@cross_origin(origins='*', methods=['POST'])
def price_prediction():
    validated_request = validate_prediction_request(request)

    if 'error' in validated_request:
        abort(validated_request['error']['code'], validated_request['error']['msg'])

    prediction = get_prediction(validated_request)
    if prediction:
        json_data = json_dumps({'price': prediction})

        response = make_response(json_data, 200)
        response.headers['Content-type'] = 'application/json'

        return response

    abort(500, 'Internal server error. Please try again later')


@api_bp.route('/api/pricePredictionParamValues', methods=['GET'])
@cross_origin(origins='*', methods=['GET'])
def price_prediction_param_values():
    param_values = allowed_prediction_features()
    json_data = json_dumps(param_values)

    response = make_response(json_data, 200)
    response.headers['Content-Type'] = 'application/json'

    return response
