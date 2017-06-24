from flask import Flask, jsonify, abort, make_response, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address, get_ipaddr

from Amiibo import AmiiboManager

app = Flask(__name__)
amiiboManager = AmiiboManager.amiiboManager()

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

# Handle 404 as json or else Flash will use html as default.
@app.errorhandler(404)
@limiter.exempt
def not_found(e):
    return make_response(jsonify(error=e.description, code=404), 404)

# Handle 429 error.
@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(jsonify(error="ratelimit exceeded %s" % e.description, code=429))

# remove limit for local ip.
@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == "127.0.0.1"

# Build the amiibo list.
def buildAmiibo(amiibo):
    headValue = amiibo.getHead()
    tailValue = amiibo.getTail()
    typeValue = amiiboManager.getAmiiboType(amiibo)[0]

    result = {}
    result.update({"name": amiibo.getName()})
    result.update({"head": headValue.lower()})
    result.update({"tail": tailValue.lower()})
    result.update({"type": typeValue.lower()})
    result.update({"gameSeries": amiiboManager.getAmiiboGameSeries(amiibo)[0]})
    result.update({"amiiboSeries": amiiboManager.getAmiiboSeries(amiibo)[0]})
    result.update({"character": amiiboManager.getAmiiboCharacter(amiibo)[0]})
    result.update({"image": "https://raw.githubusercontent.com/N3evin/AmiiboAPI/master/image/icon_" + headValue.lower() + "-" + tailValue.lower() + ".png"})
    return result;

############################### Game Series API ###############################

# gameseries API
@app.route('/api/gameseries/', methods=['GET'])
def gameSeries():
    # Parameter information
    keyParameter = request.args.get("key")
    nameParameter = request.args.get("name")

    if len(request.args)==0:
        return gameSeriesList()

    elif len(request.args) == 1:
        if keyParameter != None:
            return gameSeriesKey(keyParameter)

        elif nameParameter != None:
            return gameSeriesName(nameParameter)

        else:
            return abort(404)

    else:
        return abort(404)

# Get the list of game series
def gameSeriesList():
    series = amiiboManager.gameSeries
    result = list()

    for key, value in series.items():
        result.append({"key": key, "name": value})

    respond = jsonify({'amiibo':result})
    return respond

# Get the game series name based on the key.
def gameSeriesKey(input):
    series = amiiboManager.gameSeries
    result = list()
    for key, data in series.items():
        if (key.lower() == input.lower()):
            result= {key:data}

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo':result})
    return respond

# Get all the key belong to this game series.
def gameSeriesName(input):
    series = amiiboManager.gameSeries
    result = list()
    for key, data in series.items():
        if(data.lower() == input.lower()):
            result.append(key)

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo':result})
    return respond

############################### Amiibo Series API ###############################

# amiiboseries API
@app.route('/api/amiiboseries/', methods=['GET'])
def amiiboSeries():
    # Parameter information
    keyParameter = request.args.get("key")
    nameParameter = request.args.get("name")

    if len(request.args)==0:
        return amiiboSeriesList()

    elif len(request.args) == 1:
        if keyParameter != None:
            return amiiboSeriesKey(keyParameter)

        elif nameParameter != None:
            return amiiboSeriesName(nameParameter)

        else:
            return abort(404)

    else:
        return abort(404)

# Get the entire amiibo series.
def amiiboSeriesList():
    seriesList = amiiboManager.amiiboSeriesList
    result = list()

    for key, value in seriesList.items():
        result.append({"key": key, "name": value})

    respond = jsonify({'amiibo':result})
    return respond

# Get the amiibo series based on the key
def amiiboSeriesKey(input):
    series = amiiboManager.amiiboSeriesList
    result = list()
    for key, data in series.items():
        if (key.lower() == input.lower()):
            result.append({"key": key, "name": data})

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get the key of the amiibo series.
def amiiboSeriesName(input):
    series = amiiboManager.amiiboSeriesList
    result = list()
    for key, data in series.items():
        if (data.lower() == input.lower()):
            result.append({"key": key, "name": data})

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

############################### Type API ###############################

# type API
@app.route('/api/type/', methods=['GET'])
def amiiboType():
    # Parameter information
    keyParameter = request.args.get("key")
    nameParameter = request.args.get("name")

    if len(request.args)==0:
        return amiiboTypeList()

    elif len(request.args) == 1:
        if keyParameter != None:
            return amiiboTypeKey(keyParameter)

        elif nameParameter != None:
            return amiiboTypeName(nameParameter)

        else:
            return abort(404)

    else:
        return abort(404)

# Get all the types of amiibo available type list.
def amiiboTypeList():
    typeList = amiiboManager.typeList
    result = list()

    for key, value in typeList.items():
        result.append({"key": key, "name": value.lower()})

    respond = jsonify({'amiibo': result})
    return respond

# Get type based on key
def amiiboTypeKey(input):
    typeList = amiiboManager.typeList
    result = list()
    for key, data in typeList.items():
        if (key.lower() == input.lower()):
            result.append({"key": key, "name": data.lower()})

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get type based on name
def amiiboTypeName(input):
    typeList = amiiboManager.typeList
    result = list()
    for key, data in typeList.items():
        if (data.lower() == input.lower()):
            result.append({"key": key, "name": data.lower()})

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

############################### Character API ###############################

# character API
@app.route('/api/character/', methods=['GET'])
def amiiboCharacter():
    # Parameter information
    keyParameter = request.args.get("key")
    nameParameter = request.args.get("name")

    if len(request.args) == 0:
        return amiiboCharacterList()

    elif len(request.args) == 1:
        if keyParameter != None:
            return amiiboCharacterKey(keyParameter)

        elif nameParameter != None:
            return amiiboCharacterName(nameParameter)

        else:
            return abort(404)

    else:
        return abort(404)

# Get all the character of amiibo.
def amiiboCharacterList():
    charList = amiiboManager.charList
    result = list()

    for key, value in charList.items():
        result.append({"key": key, "name": value})

    respond = jsonify({'amiibo': result})
    return respond

# Get the character by key.
def amiiboCharacterKey(input):
    charList = amiiboManager.charList
    result = list()
    for key, data in charList.items():
        if (key.lower() == input.lower()):
            result.append({"key": key, "name": data})

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get the character by name.
def amiiboCharacterName(input):
    charList = amiiboManager.charList
    result = list()
    for key, data in charList.items():
        if (data.lower() == input.lower()):
            result.append({"key":key, "name": data})

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

############################### Amiibo API ###############################

# Get the amiibo
@app.route('/api/amiibo/', methods=['GET'])
def amiibo():
    # Parameter information
    typeParameter = request.args.get("type")
    gameSeriesParameter = request.args.get("gameseries")
    seriesParameter = request.args.get("series")
    characterParameter = request.args.get("character")
    nameParameter = request.args.get("name")
    IdParameter = request.args.get("id")

    if len(request.args) == 0:
        return amiiboList()

    elif len(request.args) == 1:
        if typeParameter != None:
            return amiiboTypeData(typeParameter)

        elif nameParameter != None:
            return amiiboName(nameParameter)

        elif IdParameter != None:
            return amiiboId(IdParameter)

        elif gameSeriesParameter != None:
            return amiiboGameSeriesData(gameSeriesParameter)

        elif seriesParameter != None:
            return amiiboSeriesData(seriesParameter)

        elif characterParameter != None:
            return amiiboCharacterData(characterParameter)

        else:
            return abort(404)

    else:
        return abort(404)

# Get all amiibo available
def amiiboList():
    amiiboList = amiiboManager.amiiboList
    result = list()

    for data in amiiboList:
        result.append(buildAmiibo(data))

    respond = jsonify({'amiibo': result})
    return respond

# Get the amiibo from name
def amiiboName(input):
    amiiboList = amiiboManager.amiiboList
    result = list()

    for data in amiiboList:
        if(data.getName().lower() == input.lower()):
            result.append(buildAmiibo(data))

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get the amiibo from id
def amiiboId(input):
    amiiboList = amiiboManager.amiiboList
    result = list()

    for data in amiiboList:
        if(data.getTail().lower() == input.lower()):                              # Tail only
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
def amiiboGameSeriesData(input):
    amiiboList = amiiboManager.amiiboList
    result = list()

    for data in amiiboList:
        if(amiiboManager.getAmiiboGameSeries(data)[0].lower() == input.lower()):
            result.append(buildAmiibo(data))
        elif (amiiboManager.getAmiiboGameSeries(data)[1].lower() == input.lower()):
            result.append(buildAmiibo(data))

    if len(result) == 0:
        abort(404)

    respond = jsonify({'amiibo': result})
    return respond

# Get the amiibo base on series
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

if __name__ == "__main__":
    app.run(debug=True)