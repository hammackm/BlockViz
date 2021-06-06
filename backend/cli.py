#Python utilities to connect with the vertcoin-cli
#command line interface to connect with a running node
import os
import json
import commands as c
import time
import pdb

os.system("cd vertcoin")

def getMostRecentBlock():
    
   hash =  c.mostRecentBlockHash()
   block = c.getBlockByHash(hash)
   block = cleanBlock(block)
   
   return block

def getNMostRecentBlocks(num_blocks: int) -> None:

    hash = c.getMostRecentBlockHash()
    block = c.getBlockByHash(hash)
    block = cleanBlock(block)
    block_list = [block]

    for i in range(1,num_blocks):
        hash = block['previousblockhash']
        block = c.getBlockByHash(hash)
        block = cleanBlock(block)
        block_list.append(block)
    
    return json.dumps(block_list)

def getBlockByHeight(height: int):

    hash = c.getHashByHeight(height)

    block = c.getBlockByHash(hash)
    block = cleanBlock(block)

    return json.dumps(block)

def getBlockByHash(hash: str):

    block = c.getBlockByHash(hash)
    block = cleanBlock(block)

    return json.dumps(block)

def getTransaction(transaction_hash: str, block_hash: str):

    transaction = c.getTransactionByBlockHash(transaction_hash, block_hash)

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

    transaction = c.getTransactionByTxid(txid)
    transaction = cleanBlock(transaction)

    return json.dumps(transaction)

def getMemPool():
    return json.dumps(
        c.getMemPool()
    )

def cleanBlock(block: dict) -> dict:

    keys = block.keys()
    clean_time_keys_list = ['time', 'mediantime', 'blocktime']

    for key in clean_time_keys_list:
        if key in keys:
            block[key] = time.ctime(block[key])

    return block
