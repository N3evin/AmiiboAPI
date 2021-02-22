from flask import Blueprint, request, jsonify, abort

from amiibo.amiibo import AmiiboTypeHex
from amiibo.manager import AmiiboManager

typeApp = Blueprint("type", __name__)

amiibo_manager = AmiiboManager.getInstance()

# type API
@typeApp.route('/api/type/', methods=['GET'])
def route_api_type():
    args = request.args

    if 'key' in args:
        try:
            key = AmiiboTypeHex(args['key'].strip())
        except ValueError:
            abort(400)
        result = amiibo_manager.types.get(key)
    else:
        filters = {}
        if 'name' in args:
            filters['name'] = args['name'].strip()

        result = amiibo_manager.types.filter(**filters)
        if 'sort' in args:
            values = {
                'key': 'id',
                'name': 'name',
            }
            result = result.sort(*[
                values[value]
                for value in args['sort'].split(',')
                if value in values
            ])

    if not result:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond