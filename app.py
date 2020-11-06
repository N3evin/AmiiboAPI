#!/usr/bin/env python
# coding=utf-8
"""
@author: N3evin
@copyright: Copyright 2017, AmiiboAPI
@license: MIT License
"""
import datetime, time, colors

from rfc3339 import rfc3339

from flask import Flask, jsonify, make_response, render_template, request, g, Response
from flask_compress import Compress
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from commons.amiibo_json_encounter import AmiiboJSONEncoder
from amiibo.manager import AmiiboManager

from routes.game_series import gameseriesApp
from routes.amiibo_series import amiiboseriesApp
from routes.type import typeApp
from routes.character import characterApp
from routes.amiibo import amiiboApp


app = Flask(__name__)

application = app

# Register app blueprints
app.register_blueprint(gameseriesApp)
app.register_blueprint(amiiboseriesApp)
app.register_blueprint(typeApp)
app.register_blueprint(characterApp)
app.register_blueprint(amiiboApp)

CORS(app)
app.json_encoder = AmiiboJSONEncoder
Compress(app)

amiibo_manager = AmiiboManager.from_json()

# Set default limit for limiter.
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

@app.route('/.well-known/acme-challenge/<challenge>')
def letsencrypt_check(challenge):
    challenge_response = {
        "<challenge_token>":"<challenge_response>",
        "<challenge_token>":"<challenge_response>"
    }
    return Response(challenge_response[challenge], mimetype='text/plain')


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

# Last updated info
@app.route('/api/lastupdated/', methods=['GET'])
def route_api_last_updated():
    respond = jsonify({'lastUpdated': amiibo_manager.last_updated})
    return respond

# store the start time before request.
@app.before_request
def start_timer():
    g.start = time.time()

# log after request
@app.after_request
def log_request(response):
    if request.path == '/favicon.ico':
        return response
    elif request.path.startswith('/api') == False:
        return response

    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method, 'blue'),
        ('path', request.path, 'blue'),
        ('status', response.status_code, 'yellow'),
        ('duration', duration, 'green'),
        ('time', timestamp, 'magenta'),
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
    app.run(host='0.0.0.0', debug=True, extra_files=['database/amiibo.json'])
