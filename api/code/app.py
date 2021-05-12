from flask import Flask, request, jsonify, abort
from pymongo import MongoClient
from bson.json_util import dumps
from flaskr.model import get_prediction


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


'''@app.route('/')
def hello():
    return 'Hello everyone!'

@app.route('/db-name')
def name():
    return db.name

@app.route('/db-listings')
def get_listings():
    return to_json(db.listings_2019.find_one({"id": "1944"}))

@app.route('/prediction')
def prediction():
    latitude = request.args['latitude']
    longitude = request.args['longitude']
    print(request.__dict__.items())
    return jsonify(get_prediction(latitude, longitude))'''

if __name__ == '__main__':
    app.run()
