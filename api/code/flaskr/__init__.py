"""app factory

The only function create_app is used to initiate an app (by using the factory pattern).
This way, the app can be instantiated with different servers (development / production)
"""


from flask import Flask
import os

def create_app():
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