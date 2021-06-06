from flask import Flask
import cli

app = Flask(__name__)

@app.route('/recent/<number>')
def getNMostRecentBlocks(number):
    return cli.getNMostRecentBlocks(int(number))

@app.route('/height/<height>')
def getBlockByHeight(height):
    return cli.getBlockByHeight(height)

@app.route('/transactions/<height>')
def getTransactionsByHeight(height):
    return cli.getTransactionsByHeight(height)

@app.route('/transaction/<txid>')
def getTransactionbyTxid(txid):
    return cli.getTransactionbyTxid(txid)