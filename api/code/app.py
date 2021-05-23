from flask import Flask, request, abort
from pymongo import MongoClient
from flaskr.model import get_prediction, validate_prediction_request
from flaskr.request_helper import to_json, filter_listings
import json
import os


app = Flask(__name__)


# import database credentials from environment
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
client = MongoClient(host='mongodb',
    username=db_username,
    password=db_password,
    authSource=db_name)
db = client[db_name]


@app.route('/api/allListings', methods=['GET', 'POST'])
def all_linstings():
    keys_filter, keys_projection = filter_listings(request)
    return to_json(db.listings.find(keys_filter, keys_projection))


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

    return to_json(db.listings.find(filter, keys_projection))


@app.route('/api/pricePrediction', methods=['POST'])
def price_prediction():
    validated_request = validate_prediction_request(request)

    if 'error' in validated_request:
        abort(validated_request['error']['code'], validated_request['error']['msg'])

    prediction = get_prediction(validated_request)
    if prediction:
        return json.dumps({'price': prediction})
    
    abort(500, 'Internal server error. Please try again later')



if __name__ == '__main__':
    app.run()
