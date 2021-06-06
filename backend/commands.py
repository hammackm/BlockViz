import os
import subprocess
import pdb

def getBlockByHash(hash: str) -> str:
    return eval(
        subprocess.check_output([os.path.join(os.getcwd(), 'vertcoin', 'vertcoin-cli.exe'), 'getblock', hash, str(1)]).decode().replace('\r\n', '')
        )

def getMostRecentBlockHash() -> str:
    return subprocess.check_output([os.path.join(os.getcwd(), 'vertcoin', 'vertcoin-cli.exe'), 'getbestblockhash']).decode()[:-2] #remove \n\r from output

def getHashByHeight(height: int):
    return subprocess.check_output([os.path.join(os.getcwd(), 'vertcoin', 'vertcoin-cli.exe'), 'getblockhash', height]).decode().replace('\r\n', '')

def getTransactionByBlockHash(transaction_hash: str, block_hash: str):
    return eval(
        subprocess.check_output([os.path.join(os.getcwd(), 'vertcoin', 'vertcoin-cli.exe'), 'getrawtransaction', transaction_hash, str(1), block_hash]).decode().replace('\r\n', '').replace('true', 'True').replace('false', 'False')
        )

def getTransactionByTxid(txid):
    return eval(
        subprocess.check_output([os.path.join(os.getcwd(), 'vertcoin', 'vertcoin-cli.exe'), 'getrawtransaction', txid, str(1)]).decode().replace('\r\n', '').replace('true', 'True').replace('false', 'False')
    )

def getMemPool():
    return eval(
        subprocess.check_output([os.path.join(os.getcwd(), 'vertcoin', 'vertcoin-cli.exe'), 'getrawmempool']).decode().replace('\r\n', '')
    )