import os
import subprocess

def getBlockByHash(hash: str) -> str:
    return subprocess.check_output([os.path.join(os.getcwd(), 'vertcoin', 'vertcoin-cli.exe'), 'getblock', hash]).decode().replace('\r\n', '')

def getMostRecentBlockHash() -> str:
    return subprocess.check_output([os.path.join(os.getcwd(), 'vertcoin', 'vertcoin-cli.exe'), 'getbestblockhash']).decode()[:-2] #remove \n\r from output

def getHashByHeight(height: int):
    return subprocess.check_output([os.path.join(os.getcwd(), 'vertcoin', 'vertcoin-cli.exe'), 'getblockhash', height]).decode().replace('\r\n', '')
