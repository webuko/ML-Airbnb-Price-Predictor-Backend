import os

from flask import Blueprint, request, abort, make_response
from flask_cors import CORS, cross_origin
from flaskr.model import get_prediction, validate_prediction_request, allowed_prediction_features
from flaskr.request_helper import project_listings, validate_filter_request
from flaskr.db import mongo

from json import dumps as json_dumps
from bson.json_util import dumps as bson_dumps


api_bp = Blueprint('api', __name__)

# enable cors compatibility
CORS(api_bp)

@api_bp.route('/api/allListings', methods=['GET', 'POST'])
@cross_origin(origins='*', methods=['GET', 'POST'])
def all_listings():
    projected_request = project_listings(request)
    if 'error' in projected_request:
        abort(projected_request['error']['code'], projected_request['error']['msg'])

    keys_filter, keys_projection = projected_request['keys_filter'], projected_request['keys_projection']

    json_data = bson_dumps(mongo.db.listings.find(keys_filter, keys_projection))

    response = make_response(json_data, 200)
    response.headers['Content-type'] = 'application/json'

    return response


@api_bp.route('/api/filterListings', methods=['POST'])
@cross_origin(origins='*', methods=['POST'])
def filtered_listings():
    validated_request = validate_filter_request(request)
    if 'error' in validated_request:
         abort(validated_request['error']['code'], validated_request['error']['msg'])
    
    keys_filter = validated_request['keys_filter']

    force_GET = request.json.get('fields') is None
    projected_request = project_listings(request, force_GET)
    if 'error' in projected_request:
        abort(projected_request['error']['code'], projected_request['error']['msg'])

    keys_projection = projected_request['keys_projection']

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


@api_bp.route('/api/avgPricePerNeighbourhood', methods=['GET', 'POST'])
@cross_origin(origins='*', methods=['GET', 'POST'])
def avg_price_neighbourhood():

    pipeline = [
        {
            "$group": 
            {
                "_id":"$neighbourhood", 
                "avgPrice": {"$avg":"$price"}
            }
        }
    ]

    if request.method == 'POST' and request.json and request.json.get('criteria'):
            validated_request = validate_filter_request(request)
            if 'error' in validated_request:
                abort(validated_request['error']['code'], validated_request['error']['msg'])
    
            keys_filter = validated_request['keys_filter']
            pipeline.insert(0, {"$match": keys_filter})

    json_data = bson_dumps(mongo.db.listings.aggregate(pipeline))

    response = make_response(json_data, 200)
    response.headers['Content-Type'] = 'application/json'

    return response