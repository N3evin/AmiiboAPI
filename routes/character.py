from flask import Blueprint, request, jsonify, abort

from amiibo.amiibo import CharacterHex
from amiibo.manager import AmiiboManager

characterApp = Blueprint("character", __name__)

amiibo_manager = AmiiboManager.getInstance()

# character API
@characterApp.route('/api/character/', methods=['GET'])
def route_api_character():
    args = request.args

    if 'key' in args:
        try:
            key = CharacterHex(args['key'].strip())
        except ValueError:
            abort(400)
        result = amiibo_manager.characters.get(key)
    else:
        filters = {}
        if 'name' in args:
            filters['name'] = args['name'].strip()

        result = amiibo_manager.characters.filter(**filters)
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