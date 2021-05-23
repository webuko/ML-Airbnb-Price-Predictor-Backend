from flask import abort
from bson.json_util import dumps


def to_json(data):
    return dumps(data)


DEFAULT_RETURN_KEYS = [
    'id', 'name', 'description', 'price',
    'picture_url', 'bedrooms', 'bathrooms',
    'accommodates', 'property_type', 'room_type',
    'neighbourhood', 'longitude', 'latitude',
]


def filter_listings(request, force_GET=False):
    if request.method == 'POST' and not force_GET:
        if not request.json.get('fields'):
            abort(400, 'fields parameter missing')

        if not isinstance(request.json['fields'], list):
            abort(400, 'Request data must be provided as array of keys')
        force_fields = False
        if request.json.get('force_fields'):
            if not isinstance(request.json['force_fields'], bool):
                abort(400, 'force_field parameter must be provided as bool')
            force_fields = request.json['force_fields']

        keys_projection = {str(key): 1 for key in request.json['fields']}
        keys_projection['_id'] = 0
        keys_filter = {}
        if force_fields:
            keys_filter = {str(key): {"$exists": 1} for key in request.json['fields']}
    else:
        keys_projection = {k: 1 for k in DEFAULT_RETURN_KEYS}
        keys_projection['_id'] = 0
        keys_filter = {}

    return keys_filter, keys_projection
