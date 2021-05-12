from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from flaskr.model import get_prediction


app = Flask(__name__)

'''DOMAIN = "localhost"
PORT = 27017
client = MongoClient(
    host = DOMAIN + ":" + str(PORT),
)'''

client = MongoClient(host='mongodb',
                     username='airbnb-user', 
                     password='pass',
                    authSource='airbnb')
db = client['airbnb']

def to_json(data):
    return dumps(data)


@app.route('/api/allListings')
def all_linstings():
    return to_json(db.listings.find({}))

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
