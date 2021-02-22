from flask import Blueprint, request, jsonify, abort

from amiibo.amiibo import AmiiboSeriesHex
from amiibo.manager import AmiiboManager

amiiboseriesApp = Blueprint("amiiboseries", __name__)

amiibo_manager = AmiiboManager.getInstance()

# amiiboseries API
@amiiboseriesApp.route('/api/amiiboseries/', methods=['GET'])
def route_api_amiibo_series():
    args = request.args

    if 'key' in args:
        try:
            key = AmiiboSeriesHex(args['key'].strip())
        except ValueError:
            abort(400)
        result = amiibo_manager.amiibo_series.get(key)
    else:
        filters = {}
        if 'name' in args:
            filters['name'] = args['name'].strip()

        result = amiibo_manager.amiibo_series.filter(**filters)
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