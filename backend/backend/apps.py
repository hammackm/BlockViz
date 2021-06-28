from django.apps import AppConfig
from . import cli
import json

db_to_rpc_block_map = {
    'hash':'hash',
    'nexthash':'nextblockhash',
    'prevhash':'previousblockhash',
    'confirmations':'confirmations',
    'numtransactions':'nTx',
    'height':'height',
    'merkleroot':'merkleroot',
    'minedby':'',
    'timestamp':'time',
    'difficulty':'difficulty',
    'size':'size',
    'nonce':'nonce',
    'version':'version',
    'bits':'bits',
    'netexchanged':'',
    'json':''
}

db_to_rpc_tx_map = {
    'id':'txid',
    'block':'blockhash',
    'coinbase':'',
    'timestamp':'time',
    'size':'size',
    'confirmations':'confirmations',
    '':'',
    '':'',
    '':'',
    '':'',
    '':'',
    '':''
}

class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):
        '''
        #update the database with all the latest blocks, transactions, and wallets since the last entry in the database
        from .models import Block, Transaction, Address  # or...

        def updateDB(height):
            
            block_dict = json.loads(cli.getBlockByHeight(height))

            block = Block(
                hash= block_dict[db_to_rpc_block_map['hash']], 
                nexthash= block_dict[db_to_rpc_block_map['nexthash']], 
                prevhash= block_dict[db_to_rpc_block_map['prevhash']], 
                numtransactions= block_dict[db_to_rpc_block_map['numtransactions']], 
                height= block_dict[db_to_rpc_block_map['height']], 
                merkleroot= block_dict[db_to_rpc_block_map['merkleroot']], 
                minedby= block_dict[db_to_rpc_block_map['minedby']], 
                timestamp= block_dict[db_to_rpc_block_map['timestamp']], 
                difficulty= block_dict[db_to_rpc_block_map['difficulty']], 
                size= block_dict[db_to_rpc_block_map['size']], 
                nonce= block_dict[db_to_rpc_block_map['nonce']], 
                version= block_dict[db_to_rpc_block_map['version']], 
                bits= block_dict[db_to_rpc_block_map['bits']], 
                netexchanged= block_dict[db_to_rpc_block_map['netexchanged']], 
                json= block_dict
            )

            block.save()

            for txid in block_dict['tx']:
                transaction_dict = json.loads(cli.getTransactionbyTxid(txid))

                inputtxids = [vin['txid'] for vin in transaction_dict['vin']]
                address_amt_map = {}
                inputaddresses = []
                outputaddresses = []

                for vin in inputtxids:
                    if not vin['coinbase']:
                        vin_tx_dict = json.loads(cli.getTransactionbyTxid(vin['txid']))
                        in_addr = vin_tx_dict['vout'][vin['vout']]['scriptPubKey']['addresses'][0]
                        in_amt = vin_tx_dict['vout'][vin['vout']]['value']

                        inputaddresses.append(in_addr)
                        address_amt_map[in_addr] = in_amt
                    else:
                        pass

                for vout in transaction_dict['vout']:
                    out_addr = vout['scriptPubKey']['addressess'][0]
                    out_amt = vout['value']

                    outputaddresses.append(out_addr)
                    address_amt_map[out_addr] = out_amt


                netexchanged = sum(address_amt_map.values())

                transaction = Transaction(
                    id= transaction_dict[db_to_rpc_tx_map['id']], 
                    block= transaction_dict[db_to_rpc_tx_map['block']], 
                    coinbase= coinbase, 
                    inputtxids= inputtxids, 
                    inputaddresses= inputaddresses, 
                    outputaddresses= outputaddresses, 
                    addressmap= address_amt_map, 
                    size= transaction_dict[db_to_rpc_tx_map['size']], 
                    timestamp= transaction_dict[db_to_rpc_tx_map['timestamp']], 
                    netexchanged= netexchanged, 
                    confirmations= transaction_dict[db_to_rpc_tx_map['confirmations']], 
                    json= transaction_dict
                )
                transaction.save()

                #if the address is not in the db, add it
                #if it is already in the db, update the balance, sent, received, numtransactions, transactions, tx_where_sent, tx_where_received
                for addr in inputaddresses:
                    if Address.objects.filter(pk=addr).exists():
                        addr_model = Address.objects.get(pk=addr)
                        addr_model
                        #update
                    else:
                        #create new entry


        
        last_block_height_stored = 
        current_block_height = json.loads(cli.getMostRecentBlock())['height']

        for height in range(last_block_height_stored+1, current_block_height+1):
            updateDB(height)
        '''
        pass
