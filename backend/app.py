from flask import Flask
import cli

app = Flask(__name__)

@app.route('/recent/<number>')
def getMostRecentDynamic(number):
    return cli.getMostRecentNBlocksDynamically(int(number))

@app.route('/height/<height>')
def getBlockByHeight(height):
    return cli.getBlockByHeight(height)