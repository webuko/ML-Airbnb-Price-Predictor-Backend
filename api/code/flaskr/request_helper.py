from flask import abort


# this constant defines the default keys that are retrieved from the db
DEFAULT_RETURN_KEYS = [
    'id', 'name', 'description', 'price',
    'host_name', 'host_picture_url', 'picture_url',
    'bedrooms', 'bathrooms','bedrooms', 'accommodates',
    'property_type', 'room_type', 'neighbourhood',
    'longitude', 'latitude', 'city'
    ]

ALLOWED_CRITERIA = {
        'price': 'num',
        'bedrooms': 'num',
        'bathrooms': 'num',
        'accommodates': 'num',
        'property_type': 'str',
        'room_type': 'str',
        'neighbourhood': 'str'
    }


def project_listings(request, force_GET=False):
    """Loads an encoder and then encodes the given value

        :param request: the request object sent by the user
        :type: flask.request
        :param force_GET: allows to retrieve default filter and projection keys in case of a POST request
        :type: boolean, optional

        :returns: a tuple containing the filter and projection keys used to retrieve data
        :rtype: tuple
    """

    if request.method == 'POST' and not force_GET:
        if not request.json.get('fields'):
            return {'error': {'code': 400, 'msg': 'fields parameter missing'}}

        if not isinstance(request.json['fields'], list):
            return {'error': {'code': 400, 'msg': 'Request data must be provided as array of keys'}}

        force_fields = False
        if request.json.get('force_fields'):
            if not isinstance(request.json['force_fields'], bool):
                return {'error': {'code': 400, 'msg': 'force_field parameter must be provided as bool'}}
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

    return {'keys_filter': keys_filter, 'keys_projection': keys_projection}


def validate_filter_request(request):
    """Validates a request for filtering listings from the database.

    :param request: the request object sent by the user
    :type: flask.request
    :returns: a dictionary containing the validated request in the form of filtering keys (error and error msg in case of an error)
    :rtype: dict
    """

    abort_msg = 'filter criteria is not correctly provided'
    keys_filter = {}

    if not request.json or not isinstance(request.json, dict):
        return {'error': {'code': 400, 'msg': 'Request data must be transmitted as JSON object'}}

    if not 'criteria' in request.json:
        return {'error': {'code': 400, 'msg': 'criteria parameter missing'}}

    for criteria, t in ALLOWED_CRITERIA.items():
        el = request.json['criteria'].get(criteria, None)
        if not el:
            continue

        if t == 'num':
            if not isinstance(el, list) or \
                    len(el) != 2 or \
                    (not str(el[0]).isdigit() or not str(el[1]).isdigit()):
                return {'error': {'code': 400, 'msg': abort_msg}}
            keys_filter[criteria] = {'$gte': el[0], '$lte': el[1]}
        else:
            if not isinstance(el, list) or \
                    len([e for e in el if str(e).isdigit()]) > 0:
                return {'error': {'code': 400, 'msg': abort_msg}}
            keys_filter[criteria] = {'$in': el}

    return {'keys_filter': keys_filter}
