#Python utilities to connect with the vertcoin-cli
#command line interface to connect with a running node
import json
import time
import requests

with open("./backend/vertcoin_node_config.json") as config_file:
    config = json.load(config_file)

def rpcCommand(command, args=[]):

    url = r'http://' + config['rpc']['username'] + ':' + config['rpc']['password'] + '@' + config['rpc']['host'] + ':' + config['rpc']['port'] + r'/' #need to error check this statement... including '@' in the password may cause this to fail
    body = '{"jsonrpc":"1.0","id":"curltest","method":"' + command + '","params":' + str(args).replace("\'", '"') + '}'
    body = body.encode()
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    r = requests.post(url = url, data=body, headers=headers)

    response = cleanRPCReponse(r.text)
    response = eval(response)
    return response

def cleanRPCReponse(response):

    response = response.replace('\n', '')
    response = response.replace('null', '0')
    response = response.replace('true', 'True')
    response = response.replace('false', 'False')

    return response

def getMostRecentBlock():

    hash = rpcCommand('getbestblockhash')['result']
    block = rpcCommand('getblock', [hash, 1])['result']
    block = cleanBlock(block)
   
    return block #dont need json dumps ?

def getNMostRecentBlocks(num_blocks: int) -> None:

    hash = rpcCommand('getbestblockhash')['result']
    block = rpcCommand('getblock', [hash, 1])['result']
    block = cleanBlock(block)
    block_list = [block]

    for i in range(1,num_blocks):
        hash = block['previousblockhash']
        block = rpcCommand('getblock', [hash, 1])['result']
        block = cleanBlock(block)
        block_list.append(block)
    
    return json.dumps(block_list)

def getBlockByHeight(height: int):

    height = int(height)
    hash = rpcCommand('getblockhash', [height])['result']
    block = rpcCommand('getblock', [hash, 1])['result']
    block = cleanBlock(block)

    return json.dumps(block)

def getBlockByHash(hash: str):

    block = rpcCommand('getblock', [hash, 1])['result']
    block = cleanBlock(block)

    return json.dumps(block)

def getTransaction(transaction_hash: str, block_hash: str):

    transaction = rpcCommand('getrawtransaction', [transaction_hash, 1, block_hash])['result']

    return json.dumps(transaction)

def getTransactionsByHeight(height: int):

    block = eval(getBlockByHeight(height))
    block_hash = block['hash']
    tx_list = block['tx']
    tx_objects_list = []

    for tx_hash in tx_list:
        tx = getTransaction(tx_hash, block_hash)
        tx = tx.replace('true', 'True')
        tx = tx.replace('false', 'False')
        tx = eval(tx)
        tx_objects_list.append(tx)

    return json.dumps(tx_objects_list)

def getTransactionbyTxid(txid: str):

    transaction = rpcCommand('getrawtransaction', [txid, 1])['result']
    transaction = cleanBlock(transaction)

    return json.dumps(transaction)

def getMemPool():

    mempool = rpcCommand('getrawmempool')['result']

    return json.dumps(mempool)

def cleanBlock(block: dict) -> dict:

    keys = block.keys()
    clean_time_keys_list = ['time', 'mediantime', 'blocktime']

    for key in clean_time_keys_list:
        if key in keys:
            block[key] = time.ctime(block[key])

    return block