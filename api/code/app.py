from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
from bson.json_util import dumps
from flaskr.model import get_prediction
import json


app = Flask(__name__)

client = MongoClient(host='mongodb',
                     username='airbnb-user', 
                     password='pass',
                    authSource='airbnb')
db = client['airbnb']

def to_json(data):
    return dumps(data)


@app.route('/api/allListings', methods=['GET', 'POST'])
def all_linstings():
    if request.method == 'POST':
        if request.get_json():
            if not isinstance(request.json, list):
                abort(400, 'Request data must be provided as array of keys')
            
            keys_projection = {str(key): 1 for key in request.json}
            keys_projection['_id'] = 0
            keys_filter = {str(key): {"$exists": 1} for key in request.json}
        else:
            abort(400, 'Request data must have content-type application/json')
    else:
        keys_projection = {
            '_id': 0,
            'name': 1,
            'price': 1,
            'longitude': 1,
            'latitude': 1,
            'description': 1,
            'picture_url': 1
        }
        keys_filter = {
            'name': {'$exists': 1},
            'price': {'$exists': 1},
            'longitude': {'$exists': 1},
            'latitude': {'$exists': 1},
            'description': {'$exists': 1},
            'picture_url': {'$exists': 1},
        }
    
    return to_json(db.listings.find(keys_filter, keys_projection))


@app.route('/api/filterListings', methods=['POST'])
def filter_listings():
    abort_msg = 'Provided filter criteria is not correctly provided'
    filter = {}

    allowed_criteria = {
       'price': 'num',
       'bedrooms': 'num',
       'bathrooms': 'num',
       'accomodates': 'num',
       'property_type': 'str',
       'room_type': 'str',
       'neighbourhood': 'str'
    }

    for criteria, type in allowed_criteria.items():
        if request.form.get(criteria):
            try:
                el = json.loads(request.form[criteria])
            except ValueError as e:
                abort(400, abort_msg)
            
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

    return to_json(db.listings.find(filter))


if __name__ == '__main__':
    app.run()
