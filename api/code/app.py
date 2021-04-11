from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from flaskr.model import get_prediction

app = Flask(__name__)

DOMAIN = "localhost"
PORT = 27017

client = MongoClient(
    host = DOMAIN + ":" + str(PORT)
)

db = client["berlinAirbnb"]

def to_json(data):
    return dumps(data)

@app.route('/')
def hello():
    return 'Hello everyone!'

@app.route('/db-name')
def name():
    return db.name

@app.route('/db-listings')
def get_listings():
    return to_json(db.listings_2019.find_one({"id": "1944"}))

@app.route('/model')
def prediction():
    return jsonify(get_prediction(
        request.form['latitude'],
        request.form['longitude'],
        request.form['property_type'],
        request.form['room_type'],
        request.form['bedrooms'],
        request.form['guests_included'],
        ))

if __name__ == '__main__':
    app.run()
