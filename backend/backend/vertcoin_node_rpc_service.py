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
    response_dict = eval(response)
    return response_dict

def cleanRPCReponse(response):

    response = response.replace('\n', '') \
        .replace('null', '0') \
        .replace('true', 'True') \
        .replace('false', 'False')

    return response

def getMostRecentBlock():

    hash = rpcCommand('getbestblockhash')['result']
    block_dict = rpcCommand('getblock', [hash, 1])['result']
    block_dict = cleanBlock(block_dict)
   
    return block_dict #dont need json dumps ?

def getNMostRecentBlocks(num_blocks: int) -> None:

    hash = rpcCommand('getbestblockhash')['result']
    block_dict = rpcCommand('getblock', [hash, 1])['result']
    block_dict = cleanBlock(block_dict)
    block_list = [block_dict]

    for i in range(1,num_blocks):
        hash = block_dict['previousblockhash']
        block_dict = rpcCommand('getblock', [hash, 1])['result']
        block_dict = cleanBlock(block_dict)
        block_list.append(block_dict)
    
    return json.dumps(block_list)

def getBlockByHeight(height: int):

    height = int(height)
    hash = rpcCommand('getblockhash', [height])['result']
    block_dict = rpcCommand('getblock', [hash, 1])['result']
    block_dict = cleanBlock(block_dict)

    return json.dumps(block_dict)

def getBlockByHash(hash: str):

    block_dict = rpcCommand('getblock', [hash, 1])['result']
    block_dict = cleanBlock(block_dict)

    return json.dumps(block_dict)

def getTransaction(transaction_hash: str, block_hash: str):

    transaction_dict = rpcCommand('getrawtransaction', [transaction_hash, 1, block_hash])['result']

    return json.dumps(transaction_dict)

def getTransactionsByHeight(height: int):

    block_dict = eval(getBlockByHeight(height))
    block_hash = block_dict['hash']
    tx_list = block_dict['tx']
    tx_dict_list = []

    for tx_hash in tx_list:
        tx_dict = getTransaction(tx_hash, block_hash)
        tx_dict = tx_dict.replace('true', 'True') \
            .replace('false', 'False')
        tx_dict = eval(tx_dict)
        tx_dict_list.append(tx_dict)

    return json.dumps(tx_dict_list)

def getTransactionbyTxid(txid: str):

    transaction_dict = rpcCommand('getrawtransaction', [txid, 1])['result']
    transaction_dict = cleanBlock(transaction_dict)
    return json.dumps(transaction_dict)

def getMemPool():

    mempool_dict = rpcCommand('getrawmempool')['result']

    return json.dumps(mempool_dict)

def cleanBlock(block: dict) -> dict:

    keys = block.keys()
    clean_time_keys_list = ['time', 'mediantime', 'blocktime']

    for key in clean_time_keys_list:
        if key in keys:
            block[key] = time.ctime(block[key])

    return block