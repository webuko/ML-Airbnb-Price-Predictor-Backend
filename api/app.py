from flask import Flask
from pymongo import MongoClient


app = Flask(__name__)

# db connection
client = MongoClient(
    host='mongodb',
    port=27017,
    username='airbnb-user',
    password='pass',
    authSource='airbnb'
)

@app.route('/')
def hello():
    return 'Hello World!'