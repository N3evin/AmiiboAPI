from flask import Flask, jsonify, abort, make_response, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from Amiibo import AmiiboManager

app = Flask(__name__)
amiiboManager = AmiiboManager.amiiboManager()

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1 per day"]
)

# Index
@app.route('/')
@limiter.exempt
def index():
    return render_template('home.html')

@app.route('/docs/')
@limiter.exempt
def documentation():
    return render_template('docs.html')

@app.route('/faq/')
@limiter.exempt
def faqPage():
    return render_template('faq.html')

# Handle 404 as json or else Flash will use html as default.
@app.errorhandler(404)
@limiter.exempt
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Get the list of game series
@app.route('/api/gameseries/', methods=['GET'])
def gameSeriesList():
    gameSeries = amiiboManager.gameSeries
    result = list()

    for key, value in gameSeries.items():
        result.append({"key": key, "name": value})

    respond = jsonify({'amiibo':result})
    return respond

# Get all the key belong to this game series.
@app.route('/api/gameseries/<string:input>/', methods=['GET'])
def gameSeries(input):
    series = amiiboManager.gameSeries
    result = list()
    for key, data in series.items():
        if(data.lower() == input.lower()):
            result.append(key)
        elif (key.lower() == input.lower()):
            result= {key:data}

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo':result})
    return respond

# Get the list of amiibo series
@app.route('/api/amiiboseries/', methods=['GET'])
def amiiboSeriesList():
    seriesList = amiiboManager.amiiboSeriesList
    result = list()

    for key, value in seriesList.items():
        result.append({"key": key, "name": value})

    respond = jsonify({'amiibo':result})
    return respond

# Get all the key belong to this amiibo series.
@app.route('/api/amiiboseries/<string:input>/', methods=['GET'])
def amiiboSeries(input):
    series = amiiboManager.amiiboSeriesList
    result = list()
    for key, data in series.items():
        if (key.lower() == input.lower()):
            result.append({"key": key, "name": data})
        elif (data.lower() == input.lower()):
            result.append({"key": key, "name": data})

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get all the types of amiibo available type list.
@app.route('/api/type/', methods=['GET'])
def amiiboTypeList():
    typeList = amiiboManager.typeList
    result = list()

    for key, value in typeList.items():
        result.append({"key": key, "name": value})

    respond = jsonify({'amiibo': result})
    return respond

# Get a list of value for that type.
@app.route('/api/type/<string:input>/', methods=['GET'])
def amiiboType(input):
    typeList = amiiboManager.typeList
    result = list()
    for key, data in typeList.items():
        if (key.lower() == input.lower()):
            result.append({"key": key, "name": data})
        elif (data.lower() == input.lower()):
            result.append({"key": key, "name": data})

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get all the character of amiibo.
@app.route('/api/character/', methods=['GET'])
def amiiboCharacterList():
    charList = amiiboManager.charList
    result = list()

    for key, value in charList.items():
        result.append({"key": key, "name": value})

    respond = jsonify({'amiibo': result})
    return respond

# Get the character value.
@app.route('/api/character/<string:input>/', methods=['GET'])
def amiiboCharacter(input):
    charList = amiiboManager.charList
    result = list()
    for key, data in charList.items():
        if (key.lower() == input.lower()):
            result.append({"key":key, "name": data})
        elif (data.lower() == input.lower()):
            result.append({"key": key, "name": data})

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get the amiibo
@app.route('/api/amiibo/', methods=['GET'])
def amiibo():
    amiiboList = amiiboManager.amiiboList
    result = list()

    for data in amiiboList:
        result.append(buildAmiibo(data))

    respond = jsonify({'amiibo': result})
    return respond

# Get the amiibo from value
@app.route('/api/amiibo/<string:input>/', methods=['GET'])
def amiiboValueData(input):
    amiiboList = amiiboManager.amiiboList
    result = list()

    for data in amiiboList:
        if(data.getName().lower() == input.lower()):                                # Name only
            result.append(buildAmiibo(data))
        elif(data.getTail().lower() == input.lower()):                              # Tail only
            result.append(buildAmiibo(data))
        elif(data.getHead().lower() == input.lower()):                              # Head only
            result.append(buildAmiibo(data))
        elif((data.getHead().lower() + data.getTail().lower()) == input.lower()):     # head + tail
            result.append(buildAmiibo(data))

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get the amiibo base on type
@app.route('/api/amiibo/type/<string:input>/', methods=['GET'])
def amiiboTypeData(input):
    amiiboList = amiiboManager.amiiboList
    typeList = amiiboManager.typeList
    result = list()

    #Check if is hex:
    if("0x" in input.lower()):
        value = typeList.get(input.lower())

    for data in amiiboList:
        if(amiiboManager.getAmiiboType(data)[0].lower() == input.lower()):
            result.append(buildAmiibo(data))
        elif (amiiboManager.getAmiiboType(data)[1].lower() == input.lower()):
            result.append(buildAmiibo(data))

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get the amiibo base on gameseries
@app.route('/api/amiibo/gameseries/<string:input>/', methods=['GET'])
def amiiboGameSeriesData(input):
    amiiboList = amiiboManager.amiiboList
    result = list()

    for data in amiiboList:
        print(amiiboManager.getAmiiboGameSeries(data)[1])
        if(amiiboManager.getAmiiboGameSeries(data)[0].lower() == input.lower()):
            result.append(buildAmiibo(data))
        elif (amiiboManager.getAmiiboGameSeries(data)[1].lower() == input.lower()):
            result.append(buildAmiibo(data))

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get the amiibo base on series
@app.route('/api/amiibo/amiiboseries/<string:input>/', methods=['GET'])
def amiiboSeriesData(input):
    amiiboList = amiiboManager.amiiboList
    result = list()

    for data in amiiboList:
        if(amiiboManager.getAmiiboSeries(data)[0].lower() == input.lower()):
            result.append(buildAmiibo(data))
        elif (amiiboManager.getAmiiboSeries(data)[1].lower() == input.lower()):
            result.append(buildAmiibo(data))

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get the amiibo base on character
@app.route('/api/amiibo/character/<string:input>/', methods=['GET'])
def amiiboCharacterData(input):
    amiiboList = amiiboManager.amiiboList
    result = list()

    for data in amiiboList:
        if(amiiboManager.getAmiiboCharacter(data)[0].lower() == input.lower()):
            result.append(buildAmiibo(data))
        elif (amiiboManager.getAmiiboCharacter(data)[1].lower() == input.lower()):
            result.append(buildAmiibo(data))

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Build the amiibo list.
def buildAmiibo(amiibo):
    result = {}
    result.update({"name": amiibo.getName()})
    result.update({"head": amiibo.getHead().lower()})
    result.update({"tail": amiibo.getTail().lower()})
    result.update({"type": amiiboManager.getAmiiboType(amiibo)[0]})
    result.update({"gameSeries": amiiboManager.getAmiiboGameSeries(amiibo)[0]})
    result.update({"amiiboSeries": amiiboManager.getAmiiboSeries(amiibo)[0]})
    result.update({"character": amiiboManager.getAmiiboCharacter(amiibo)[0]})
    result.update({"image": "http://amiibo.life/nfc/"+amiibo.getHead()+"-"+amiibo.getTail()+"/image"})
    return result;

@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == "127.0.0.1"

if __name__ == "__main__":
    app.run(debug=True)