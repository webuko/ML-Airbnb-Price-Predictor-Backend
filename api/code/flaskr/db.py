'''
PyMongo instance is initialized here (and not in flaskr/__init__.py) to prevent a circular import.
To use this instance import it the following way (in files): from flaskr.db import mongo
'''
from flask_pymongo import PyMongo
mongo = PyMongo()