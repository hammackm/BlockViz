from flask import Flask
import cli

app = Flask(__name__)

@app.route('/recent/block/<number>')
def getNMostRecentBlocks(number):
    return cli.getNMostRecentBlocks(int(number))

@app.route('/recent/transaction/<number>')
def getNMostRecentTransactions(number):
    return cli.getNMostRecentBlocks(int(number))

@app.route('/height/<height>')
def getBlockByHeight(height):
    return cli.getBlockByHeight(height)

@app.route('/blockhash/<hash>')
def getBlockByHash(hash):
    return cli.getBlockByHash(hash)

@app.route('/transactions/<height>')
def getTransactionsByHeight(height):
    return cli.getTransactionsByHeight(height)

@app.route('/transaction/<txid>')
def getTransactionbyTxid(txid):
    return cli.getTransactionbyTxid(txid)

@app.route('/mempool/')
def getMemPool():
    return cli.getMemPool()