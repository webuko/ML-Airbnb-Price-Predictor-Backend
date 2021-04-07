from flask import Flask, abort
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


if __name__ == '__main__':
    app.run(host='0.0.0.0')