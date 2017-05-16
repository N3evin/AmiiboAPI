from flask import Flask, send_from_directory, jsonify, abort, make_response, url_for
import requests, os, json, AmiiboManager

app = Flask(__name__)
amiiboManager = AmiiboManager.amiiboManager()

# Index
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Handle 404 as json or else Flash will use html as default.
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Get the list of game series
@app.route('/api/v1/gameseries', methods=['GET'])
def gameSeriesList():
    gameSeries = amiiboManager.gameSeries
    result = list()

    for key, value in gameSeries.items():
        result.append({"key": key, "name": value})

    respond = jsonify({'amiibo':result})
    return respond

# Get all the key belong to this game series.
@app.route('/api/v1/gameseries/<string:input>', methods=['GET'])
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
@app.route('/api/v1/amiiboseries', methods=['GET'])
def amiiboSeriesList():
    seriesList = amiiboManager.amiiboSeriesList
    result = list()

    for key, value in seriesList.items():
        result.append({"key": key, "name": value})

    respond = jsonify({'amiibo':result})
    return respond

# Get all the key belong to this amiibo series.
@app.route('/api/v1/amiiboseries/<string:input>', methods=['GET'])
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
@app.route('/api/v1/type', methods=['GET'])
def amiiboTypeList():
    typeList = amiiboManager.typeList
    result = list()

    for key, value in typeList.items():
        result.append({"key": key, "name": value})

    respond = jsonify({'amiibo': result})
    return respond

# Get a list of value for that type.
@app.route('/api/v1/type/<string:input>', methods=['GET'])
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
@app.route('/api/v1/character', methods=['GET'])
def amiiboCharacterList():
    charList = amiiboManager.charList
    result = list()

    for key, value in charList.items():
        result.append({"key": key, "name": value})

    respond = jsonify({'amiibo': result})
    return respond

# Get the character value.
@app.route('/api/v1/character/<string:input>', methods=['GET'])
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
@app.route('/api/v1/amiibo', methods=['GET'])
def amiibo():
    amiiboList = amiiboManager.amiiboList
    result = list()

    for data in amiiboList:
        result.append(buildAmiibo(data))

    respond = jsonify({'amiibo': result})
    return respond

# Get the amiibo from value
@app.route('/api/v1/amiibo/<string:input>', methods=['GET'])
def amiiboValue(input):
    amiiboList = amiiboManager.amiiboList
    result = list()

    for data in amiiboList:
        if(data.getName().lower() == input.lower()):
            result.append(buildAmiibo(data))
        elif(data.getTail().lower() == input.lower()):
            result.append(buildAmiibo(data))
        elif(data.getHead().lower() == input.lower()):
            result.append(buildAmiibo(data))

    respond = jsonify({'amiibo': result})
    return respond

# Get the amiibo
@app.route('/api/v1/amiibo/type/<string:input>', methods=['GET'])
def amiiboDataType(input):
    amiiboList = amiiboManager.amiiboList
    typeList = amiiboManager.typeList
    result = list()

    #Check if is hex:
    if("0x" in input.lower()):
        value = typeList.get(input.lower())

    for data in amiiboList:
        if(amiiboManager.getAmiiboType(data).lower() == input.lower()):
            result.append(buildAmiibo(data))

    respond = jsonify({'amiibo': result})
    return respond

# Build the amiibo list.
def buildAmiibo(amiibo):
    result = {}
    result.update({"name": amiibo.getName()})
    result.update({"head": amiibo.getHead()})
    result.update({"tail": amiibo.getTail()})
    result.update({"type": amiiboManager.getAmiiboType(amiibo)})
    result.update({"gameseries": amiiboManager.getAmiiboGameSeries(amiibo)})
    result.update({"series": amiiboManager.getAmiiboSeries(amiibo)})
    result.update({"character": amiiboManager.getAmiiboCharacter(amiibo)})
    result.update({"image": "https://raw.githubusercontent.com/Falco20019/libamiibo/master/libamiibo.images/Images/icon_" + amiibo.getHead().lower() + amiibo.getTail().lower() + ".png"})
    return result;


if __name__ == "__main__":
    app.run(debug=True)