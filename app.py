#!/usr/bin/env python
# coding=utf-8
"""
@author: N3evin
@copyright: Copyright 2017, AmiiboAPI
@license: MIT License
"""
import colors

from rfc3339 import rfc3339

from flask import Flask, jsonify, make_response, render_template, request
from flask_compress import Compress
from flask_cors import CORS

from commons.amiibo_json_encounter import AmiiboJSONEncoder
from amiibo.manager import AmiiboManager

from routes.game_series import gameseriesApp
from routes.amiibo_series import amiiboseriesApp
from routes.type import typeApp
from routes.character import characterApp
from routes.amiibo import amiiboApp
from routes.amiibofull import amiibofullApp

app = Flask(__name__)

application = app

# Register app blueprints
app.register_blueprint(gameseriesApp)
app.register_blueprint(amiiboseriesApp)
app.register_blueprint(typeApp)
app.register_blueprint(characterApp)
app.register_blueprint(amiiboApp)
app.register_blueprint(amiibofullApp)

CORS(app)
app.json_encoder = AmiiboJSONEncoder
Compress(app)

amiibo_manager = AmiiboManager.getInstance()

# Index
@app.route('/')
def index():
    return render_template('home.html')


# Documentation
@app.route('/docs/')
def documentation():
    return render_template('docs.html')


# FAQs
@app.route('/faq/')
def faqPage():
    return render_template('faq.html')

# Handle 400 as json or else Flask will use html as default.
@app.errorhandler(400)
def bad_request(e):
    return make_response(jsonify(error=e.description, code=400), 400)


# Handle 404 as json or else Flask will use html as default.
@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify(error=e.description, code=404), 404)


# Handle 429 error.
@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(jsonify(error="rate limit exceeded %s" % e.description, code=429))


# Last updated info
@app.route('/api/lastupdated/', methods=['GET'])
def route_api_last_updated():
    respond = jsonify({'lastUpdated': amiibo_manager.last_updated})
    return respond

# log after request
@app.after_request
def log_request(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/api') == False:
        return response

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method, 'blue'),
        ('path', request.path, 'blue'),
        ('status', response.status_code, 'yellow'),
        ('ip', ip, 'red'),
        ('host', host, 'red'),
        ('params', args, 'blue')
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id, 'yellow'))

    parts = []
    for name, value, color in log_params:
        part = colors.color("{}={}".format(name, value), fg=color)
        parts.append(part)
    line = " ".join(parts)

    app.logger.info(line)

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, extra_files=['database/amiibo.json', 'database/games_info.json'])
