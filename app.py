#!/usr/bin/env python
"""
@author: N3evin
@copyright: Copyright 2017, AmiiboAPI
@license: MIT License
"""
import datetime

from flask import Flask, jsonify, abort, make_response, render_template, request
from flask.json import JSONEncoder
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_compress import Compress

from amiibo.amiibo import (
    Hex,
    AmiiboHex,
    GameSeriesHex,
    CharacterHex,
    VariantHex,
    AmiiboTypeHex,
    AmiiboModelHex,
    AmiiboSeriesHex,
    Amiibo,
    AmiiboReleaseDates,
    GameSeries,
    Character,
    AmiiboType,
    AmiiboSeries,
)
from amiibo.manager import AmiiboManager
from amiibo.filterable import FilterableCollection


class AmiiboJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Hex):
            return str(obj)
        elif isinstance(obj, FilterableCollection):
            return list(obj)
        elif isinstance(obj, Amiibo):
            return {
                'name': obj.name,
                'head': str(obj.head)[2:],
                'tail': str(obj.tail)[2:],
                'type': obj.amiibo_type.name if obj.amiibo_type else None,
                'gameSeries': obj.game_series.name if obj.game_series else None,
                'amiiboSeries': obj.amiibo_series.name if obj.amiibo_series else None,
                'character': obj.character.name if obj.character else None,
                'image': "https://raw.githubusercontent.com/N3evin/AmiiboAPI/master/images/icon_{}-{}.png".format(str(obj.head)[2:], str(obj.tail)[2:]),
                'release': obj.release,
            }
        elif isinstance(obj, (GameSeries, Character, AmiiboType, AmiiboSeries)):
            return {
                'key': obj.id,
                'name': obj.name,
            }
        elif isinstance(obj, AmiiboReleaseDates):
            return {
                'na': obj.na,
                'jp': obj.jp,
                'eu': obj.eu,
                'au': obj.au,
            }
        elif isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
            return obj.isoformat()

        return super().default(obj)


app = Flask(__name__)
app.json_encoder = AmiiboJSONEncoder
Compress(app)

amiibo_manager = AmiiboManager.from_json()

# Set default limit for limter.
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["300 per day"]
)


# Index
@app.route('/')
@limiter.exempt
def index():
    return render_template('home.html')


# Documentation
@app.route('/docs/')
@limiter.exempt
def documentation():
    return render_template('docs.html')


# FAQs
@app.route('/faq/')
@limiter.exempt
def faqPage():
    return render_template('faq.html')


# Handle 400 as json or else Flask will use html as default.
@app.errorhandler(400)
@limiter.exempt
def bad_request(e):
    return make_response(jsonify(error=e.description, code=400), 400)


# Handle 404 as json or else Flask will use html as default.
@app.errorhandler(404)
@limiter.exempt
def not_found(e):
    return make_response(jsonify(error=e.description, code=404), 404)


# Handle 429 error.
@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(jsonify(error="rate limit exceeded %s" % e.description, code=429))


# remove limit for local ip.
@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == "127.0.0.1"


############################### Game Series API ###############################

# gameseries API
@app.route('/api/gameseries/', methods=['GET'])
def route_api_game_series():
    args = request.args

    if 'key' in args:
        try:
            key = GameSeriesHex(args['key'].strip())
        except ValueError:
            abort(400)
        result = amiibo_manager.game_series.get(key)
    else:
        filters = {}
        if 'name' in args:
            filters['name'] = args['name'].strip()

        result = amiibo_manager.game_series.filter(**filters)
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


############################### Amiibo Series API ###############################

# amiiboseries API
@app.route('/api/amiiboseries/', methods=['GET'])
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


############################### Type API ###############################

# type API
@app.route('/api/type/', methods=['GET'])
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


############################### Character API ###############################

# character API
@app.route('/api/character/', methods=['GET'])
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


############################### Amiibo API ###############################

# Get the amiibo
@app.route('/api/amiibo/', methods=['GET'])
def route_api_amiibo():
    args = request.args

    if 'id' in args:
        try:
            id_ = AmiiboHex(args['id'].strip())
        except ValueError:
            abort(400)
        result = amiibo_manager.amiibos.get(id_)
    else:
        filters = {}
        if 'head' in args:
            try:
                filters['head'] = Hex(args['head'].strip())
            except ValueError:
                abort(400)

        if 'tail' in args:
            try:
                filters['tail'] = Hex(args['tail'].strip())
            except ValueError:
                abort(400)

        if 'name' in args:
            filters['name'] = args['name'].strip()

        if 'gameseries' in args:
            game_series = args['gameseries'].strip()
            if game_series.startswith('0x'):
                try:
                    filters['game_series_id'] = GameSeriesHex(game_series)
                except ValueError:
                    abort(400)
            else:
                filters['game_series_name'] = game_series

        if 'character' in args:
            character = args['character'].strip()
            if character.startswith('0x'):
                try:
                    filters['character_id'] = CharacterHex(character)
                except ValueError:
                    abort(400)
            else:
                filters['character_name'] = character

        if 'variant' in args:
            try:
                filters['variant_id'] = VariantHex(args['variant'].strip())
            except ValueError:
                abort(400)

        if 'type' in args:
            amiibo_type = args['type'].strip()
            if amiibo_type.startswith('0x'):
                try:
                    filters['amiibo_type_id'] = AmiiboTypeHex(amiibo_type)
                except ValueError:
                    abort(400)
            else:
                filters['amiibo_type_name'] = amiibo_type

        if 'amiibo_model' in args:
            filters['amiibo_model_id'] = AmiiboModelHex(args['amiibo_model'].strip())

        if 'amiiboseries' in args:
            amiibo_series = args['amiiboseries'].strip()
            if amiibo_series.startswith('0x'):
                try:
                    filters['amiibo_series_id'] = AmiiboSeriesHex(amiibo_series)
                except ValueError:
                    abort(400)
            else:
                filters['amiibo_series_name'] = amiibo_series

        result = amiibo_manager.amiibos.filter(**filters)
        if 'sort' in args:
            values = {
                'id': 'id',
                'head': 'head',
                'tail': 'tail',
                'name': 'name',
                'gameseries': 'gameseries',
                'gameseries_id': 'game_series_id',
                'gameseries_name': 'game_series_name',
                'character': 'character_name',
                'character_id': 'character_id',
                'character_name': 'character_name',
                'variant': 'variant_id',
                'variant_id': 'variant_id',
                'type': 'amiibo_type_id',
                'type_id': 'amiibo_type_id',
                'type_name': 'amiibo_type_name',
                'amiibo_model': 'amiibo_model_id',
                'amiibo_model_id': 'amiibo_model_id',
                'series': 'amiibo_series_name',
                'series_id': 'amiibo_series_id',
                'series_name': 'amiibo_series_name',
                'release_na': 'release_na',
                'release_jp': 'release_jp',
                'release_eu': 'release_eu',
                'release_au': 'release_au',
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

if __name__ == "__main__":
    app.run(debug=True)
