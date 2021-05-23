from flask import Flask, request, abort, make_response
from flaskr.model import get_prediction, validate_prediction_request, allowed_prediction_features
from flaskr.request_helper import filter_listings

from pymongo import MongoClient

from json import dumps as json_dumps
from bson.json_util import dumps as bson_dumps


app = Flask(__name__)

client = MongoClient(host='mongodb',
                     username='airbnb-user', 
                     password='pass',
                    authSource='airbnb')
db = client['airbnb']


@app.route('/api/allListings', methods=['GET', 'POST'])
def all_linstings():
    keys_filter, keys_projection = filter_listings(request)
    
    json_data = bson_dumps(db.listings.find(keys_filter, keys_projection))

    response = make_response(json_data, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-type'] = 'application/json'
    
    return response


@app.route('/api/filterListings', methods=['POST'])
def filtered_listings():
    abort_msg = 'filter criteria is not correctly provided'
    filter = {}

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

    for criteria, type in allowed_criteria.items():
        el = request.json['criteria'].get(criteria, None)
        if not el:
            continue
            
        if type == 'num':
            if not isinstance(el, list) or \
                len(el) != 2 or \
                (not str(el[0]).isdigit() or not str(el[1]).isdigit()):
                abort(400, abort_msg)
            filter[criteria] = {'$gte': el[0], '$lte': el[1]}
        else:
            if not isinstance(el, list) or \
                len([e for e in el if str(e).isdigit()]) > 0:
                abort(400, abort_msg)
            filter[criteria] = {'$in': el}

    force_GET = request.json.get('fields') is None
    _, keys_projection = filter_listings(request, force_GET)

    json_data = bson_dumps(db.listings.find(filter, keys_projection))

    response = make_response(json_data, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-type'] = 'application/json'
    
    return response


@app.route('/api/pricePrediction', methods=['POST'])
def price_prediction():
    validated_request = validate_prediction_request(request)

    if 'error' in validated_request:
        abort(validated_request['error']['code'], validated_request['error']['msg'])

    prediction = get_prediction(validated_request)
    if prediction:
        json_data = json_dumps({'price': prediction})

        response = make_response(json_data, 200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-type'] = 'application/json'
    
        return response
    
    abort(500, 'Internal server error. Please try again later')


@app.route('/api/pricePredictionParamValues', methods=['GET'])
def price_prediction_param_values():
    param_values = allowed_prediction_features()
    json_data = json_dumps(param_values)

    response = make_response(json_data, 200)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-type'] = 'application/json'
    
    return response


if __name__ == '__main__':
    app.run()