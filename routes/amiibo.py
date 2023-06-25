from flask import Blueprint, request, jsonify, abort

from amiibo.amiibo import AmiiboHex, GameSeriesHex, CharacterHex, VariantHex, AmiiboTypeHex, AmiiboModelHex, AmiiboSeriesHex, Hex
from amiibo.manager import AmiiboManager
from amiibo.filterable import AmiiboCollection

amiiboApp = Blueprint("amiibo", __name__)

amiibo_manager = AmiiboManager.getInstance()

# Get the amiibo
@amiiboApp.route('/api/amiibo/', methods=['GET'])
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

        if 'switch_titleid' in args:
            filters['switch_titleid'] = args['switch_titleid']

        if 'wiiu_titleid' in args:
            filters['wiiu_titleid'] = args['wiiu_titleid']

        if '3ds_titleid' in args:
            filters['3ds_titleid'] = args['3ds_titleid']

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

        if 'amiiboSeries' in args:
            amiibo_series = args['amiiboSeries'].strip()
            if amiibo_series.startswith('0x'):
                try:
                    filters['amiibo_series_id'] = AmiiboSeriesHex(amiibo_series)
                except ValueError:
                    abort(400)
            else:
                filters['amiibo_series_name'] = amiibo_series

        result = AmiiboCollection()
        print(args)
        if 'showusage' in args:
            if filters != {}:
                result = amiibo_manager.amiibosfull.filter(**filters)
            else:
                result = amiibo_manager.amiibosfull
        elif 'showgames' in args:
            if filters != {}:
                result = amiibo_manager.amiibosfullwithoutusage.filter(**filters)
            else:
                result = amiibo_manager.amiibosfullwithoutusage
        else:
            if filters != {}:
                for amiibo in amiibo_manager.amiibosfull.filter(**filters):
                    result.add(amiibo_manager.amiibos[amiibo.id])
            else:
                result = amiibo_manager.amiibos

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

    respond = jsonify({'amiibo': result})
    return respond