#Python utilities to connect with the vertcoin-cli
#command line interface to connect with a running node
import json
from datetime import datetime
import requests
import socket, errno
import base64
import time
import pdb
from . import logging_service as log

class NodeRPCService():
    '''
    A class is used primarly because of requests.Session.
    A stateful requests.Session is needed to increase performance and to avoid bugs relating to using ports before they are released
    '''
    def __init__(self):
        self.requests_session = requests.Session()
        with open("./backend/vertcoin_node_config.json") as config_file:
            self.config = json.load(config_file)

    def rpcCommandWithSocket(self, command, params=[]):
        '''
        Now unused code to execute RPC commands with the socket module and not the requests module.
        '''
        SOCKET_POOL = list(range(50000,65000))

        host = self.config['rpc']['host']
        port = self.config['rpc']['port']

        un = self.config['rpc']['username']
        pw = self.config['rpc']['password']

        headers = """\
        POST / HTTP/1.1\r
        Content-Type: {content_type}\r
        Content-Length: {content_length}\r
        Host: {host}\r
        Authorization: {auth}\r
        Connection: close\r
        \r\n"""

        #build authorization header
        auth_str = un+':'+pw
        auth_bytes = auth_str.encode('ascii')
        base64_bytes = base64.b64encode(auth_bytes)
        auth = base64_bytes.decode('ascii')

        body = '{"jsonrpc":"1.0","id":"curltest","method":"' + command + '","params":' + str(params).replace("\'", '"') + '}'
        body_bytes = body.encode('ascii')
        header_bytes = headers.format(
            content_type="application/x-www-form-urlencoded",
            content_length=len(body_bytes),
            host=host + ":" + str(port),
            auth="Basic " + auth 
        ).encode('iso-8859-1')

        payload = header_bytes + body_bytes

        #create socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #now bind on the first available port in the pool
        for bind_port in SOCKET_POOL:
            try:
                s.bind((host, bind_port))
                break
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    log.log('WARNING', 'vertcoin_node_rpc_service', f'Could not bind to port: {bind_port}. Port is already in use')
                else:
                    log.log('WARNING', 'vertcoin_node_rpc_service', f'Could not bind to port: {bind_port}. Undocumented issue caused this')

        #Connect to remote, send, and ready for receive
        s.connect((host, int(port)))
        s.sendall(payload)
        s.setblocking(0)
        
        #Receive with timeout
        total_data=[]
        data=''
        timeout = 2

        #beginning time
        begin=time.time()
        while 1:
            #if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break
            
            #if you got no data at all, wait a little longer, twice the timeout
            elif time.time()-begin > timeout*2:
                break
            
            #recv something
            try:
                data = s.recv(8192)
                if data:
                    total_data.append(data)
                    #change the beginning time for measurement
                    begin=time.time()
                else:
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass
            
        s.close()
        #join all parts to make final string
        response = b''.join(total_data)
        response = response.decode()
        response = self.cleanRPCReponse(response)
        response_dict = eval(response)

        return response_dict


    def rpcCommand(self, command, params=[]):
        '''
        Makes a request to the node RPC server with the given commands and args
        '''
        #Create the request to send to the vertcoin node rpc service.
        url = r'http://' + self.config['rpc']['username'] + ':' + self.config['rpc']['password'] + '@' + self.config['rpc']['host'] + ':' + self.config['rpc']['port'] + r'/' #need to error check this statement... including '@' in the password may cause this to fail
        body = '{"jsonrpc":"1.0","id":"curltest","method":"' + command + '","params":' + str(params).replace("\'", '"') + '}'
        body = body.encode()
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        r = self.requests_session.post(url = url, data=body, headers=headers)

        if r.status_code == 200:
            response = self.cleanRPCReponse(r.text)
            response_dict = eval(response)

            return response_dict
        else:
            #this needs to be handled
            return {}

    def cleanRPCReponse(self, response):
        '''
        Clean the response by the RPC to have <eval> called upon it in order to turn it into a dictionary
        '''
        response = response.replace('\n', '') \
            .replace('null', '0') \
            .replace('true', 'True') \
            .replace('false', 'False')

        return response

    def getMostRecentBlock(self):
        '''
        Returns a dictionary of the latest block in the chain according to the local node.
        '''
        hash = self.rpcCommand('getbestblockhash')['result']
        block_dict = self.rpcCommand('getblock', [hash, 1])['result']
        block_dict = self.cleanBlock(block_dict)
    
        return block_dict #dont need json dumps ?

    def getMostRecentBlockHeight(self):
        '''
        Returns the height of the most recent block
        '''

        hash = self.rpcCommand('getbestblockhash')['result']
        block_dict = self.rpcCommand('getblock', [hash, 1])['result']
        height = block_dict['height']

        return height

    def getNMostRecentBlocks(self, num_blocks: int):
        '''
        Returns a list of block dictionaries—the n-most recent blocks in the chain
        '''
        hash = self.rpcCommand('getbestblockhash')['result']
        block_dict = self.rpcCommand('getblock', [hash, 1])['result']
        block_dict = self.cleanBlock(block_dict)
        block_list = [block_dict]

        for i in range(1,num_blocks):
            hash = block_dict['previousblockhash']
            block_dict = self.rpcCommand('getblock', [hash, 1])['result']
            block_dict = self.cleanBlock(block_dict)
            block_list.append(block_dict)
        
        return json.dumps(block_list)

    def getBlockByHeight(self, height: int):
        '''
        Returns the block dictionary that is associated with the input height
        '''
        height = int(height) #sometime comes in as a str?

        hash = self.rpcCommand('getblockhash', [height])['result']
        block_dict = self.rpcCommand('getblock', [hash, 1])['result']

        block_dict = self.cleanBlock(block_dict)

        return json.dumps(block_dict)

    def getBlockByHash(self, hash: str):
        '''
        Returns the block dictionary that is associated with the input hash
        '''
        block_dict = self.rpcCommand('getblock', [hash, 1])['result']
        block_dict = self.cleanBlock(block_dict)

        return json.dumps(block_dict)

    def getTransaction(self, transaction_hash: str, block_hash: str):

        transaction_dict = self.rpcCommand('getrawtransaction', [transaction_hash, 1, block_hash])['result']

        return json.dumps(transaction_dict)

    def getTransactionsByHeight(self, height: int):

        block_dict = eval(self.getBlockByHeight(height))
        block_hash = block_dict['hash']
        tx_list = block_dict['tx']
        tx_dict_list = []

        for tx_hash in tx_list:
            tx_dict = self.getTransaction(tx_hash, block_hash)
            tx_dict = tx_dict.replace('true', 'True') \
                .replace('false', 'False')
            tx_dict = eval(tx_dict)
            tx_dict_list.append(tx_dict)

        return json.dumps(tx_dict_list)

    def getTransactionbyTxid(self, txid: str):

        transaction_dict = self.rpcCommand('getrawtransaction', [txid, 1])['result']

        transaction_dict = self.cleanBlock(transaction_dict)
        return json.dumps(transaction_dict)

    def getMemPool(self):
        '''
        Returns the current MemPool (unmined transactions) of the VertCoin Node.
        '''

        mempool_dict = self.rpcCommand('getrawmempool')['result']

        return json.dumps(mempool_dict)

    def cleanBlock(self, block: dict) -> dict:
        '''
        Cleans the block dictionary—replaces unix-style int time into datetime
        '''

        keys = block.keys()
        clean_time_keys_list = ['time', 'mediantime', 'blocktime']

        for key in clean_time_keys_list:
            if key in keys:
                block[key+'stamp'] = block[key]
                block[key] = datetime.fromtimestamp(block[key]).strftime('%Y-%m-%d %H:%M:%S.%f')
                

        return block