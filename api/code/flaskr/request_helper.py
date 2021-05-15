from flask import abort
from bson.json_util import dumps
import json


def to_json(data):
    return dumps(data)


DEFAULT_RETURN_KEYS = [
    'id', 'name', 'description',
    'picture_url', 'bedrooms', 'bathrooms',
    'accommodates', 'property_type', 'room_type',
    'neighbourhood', 'longitude', 'latitude',
    ]

def filter_listings(request, force_GET=False):
    if request.method == 'POST' and not force_GET:
        if not request.form.get('fields'):
            abort(400, 'fields parameter missing')

        try:
            parsed_list = json.loads(request.form['fields'])
        except ValueError as e:
            abort(400, 'Request data must be provided as array of keys')
        if not isinstance(parsed_list, list):
              abort(400, 'Request data must be provided as array of keys')
        
        force_fields = False
        if request.form.get('force_fields'):
            try:
                parsed_bool = json.loads(request.form['force_fields'])
            except ValueError as e:
                abort(400, 'force_field parameter must be provided as bool')
            if not isinstance(parsed_bool, bool):
                abort(400, 'force_field parameter must be provided as bool')
            
            force_fields = parsed_bool
            
        keys_projection = {str(key): 1 for key in parsed_list}
        keys_projection['_id'] = 0
        keys_filter = {}
        if force_fields:
            keys_filter = {str(key): {"$exists": 1} for key in parsed_list}
    else:
        keys_projection = {k: 1 for k in DEFAULT_RETURN_KEYS}
        keys_projection['_id'] = 0
        keys_filter = {}
    
    return keys_filter, keys_projection