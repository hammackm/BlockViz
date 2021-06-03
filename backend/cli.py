#Python utilities to connect with the vertcoin-cli
#command line interface to connect with a running node
import os
import json
import commands as c
import time
os.system("cd vertcoin")

def getMostRecentBlock():
    
   hash =  c.mostRecentBlockHash()
   block = eval(c.getBlockByHash(hash))
   block = cleanBlock(block)
   
   return block

def getMostRecentNBlocksDynamically(num_blocks: int) -> None:

    hash = c.getMostRecentBlockHash()
    block = eval(c.getBlockByHash(hash))
    block = cleanBlock(block)
    block_list = [block]

    for i in range(1,num_blocks):
        hash = block['previousblockhash']
        block = eval(c.getBlockByHash(hash))
        block = cleanBlock(block)
        block_list.append(block)
    
    return json.dumps(block_list)

def getBlockByHeight(height: int):

    hash = c.getHashByHeight(height)

    block = eval(c.getBlockByHash(hash))
    block = cleanBlock(block)

    return json.dumps(block)


def cleanBlock(block: dict) -> dict:
    block['time'] = time.ctime(block['time']) #convert time to readable format
    block['transactions'] = block['nTx']
    return block
