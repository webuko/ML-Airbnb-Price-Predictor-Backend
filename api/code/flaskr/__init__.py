"""This module contains all the code that is used to make this api work."""

from flask import Flask
import os

def create_app():
    """ Creates a flask app

    This function is used to create an app (using the factory pattern).This way, 
    the app can be instantiated with different servers (development / production)

    :returns: a flask application
    :rtype: flask.app
    """

    app = Flask(__name__)

    # set configs for db
    db_username = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    app.config['MONGO_URI'] = f'mongodb://{db_username}:{db_password}@mongodb:27017/{db_name}'
    # init extensions
    from flaskr.db import mongo
    mongo.init_app(app)

    # register blueprint(s)
    from flaskr.routes import api_bp
    app.register_blueprint(api_bp)

    return app