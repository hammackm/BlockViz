import pdb
from .models import Chain, Block, Transaction, Address
import json
from . import vertcoin_node_rpc_service as rpc
from . import logging_service as log

def initialize():
    '''
    A method to be used only when the database is empty, or is not populated.
    '''

    chain_model = Chain(latestdbblockheight=0)
    chain_model.save()


def updateDatabase():
    '''
    Update the database with all the latest blocks, transactions, and wallets since the last entry in the database
    '''

    chain_model = Chain.objects.get(id=1) # IDs are 1-indexed

    latest_node_block_height = rpc.getMostRecentBlockHeight()
    latest_db_block_height = chain_model.latestdbblockheight

    for height in range(latest_db_block_height+1, latest_node_block_height):
        print('INFO', 'database_update_service', f'Updating the database with block of height {height}')
        updateDatabaseByHeight(height)


def createNewBlockEntry(block_dict: dict):
    '''
    Creates a new block entry in the database
    Updates the chain entry with the latest block height
    '''

    block_model = Block(
        hash= block_dict['hash'], 
        nexthash= block_dict['nextblockhash'], 
        prevhash= block_dict['previousblockhash'], 
        numtransactions= block_dict['nTx'], 
        height= block_dict['height'], 
        merkleroot= block_dict['merkleroot'], 
        minedby= None, 
        timestamp= block_dict['time'], 
        difficulty= block_dict['difficulty'], 
        size= block_dict['size'], 
        nonce= block_dict['nonce'], 
        version= block_dict['version'], 
        bits= block_dict['bits'], 
        netexchanged= None, 
        json= block_dict
    )

    block_model.save()

    chain_model = Chain.objects.get(id=1) #not sure if the id is 0 or 1 indexed, regardless the chain model should only ever have one entry

    if block_dict['height'] <= chain_model.latestdbblockheight:
        log.info('WARNING', 'database_update_service', 'Adding a block to the database where its height is less than or equal to the chain_models latestdbblockheight')

    chain_model.latestdbblockheight = block_dict['height']
    chain_model.save()

def createNewTransactionEntry(transaction_dict: dict):
    '''
    Creates a new transaction entry in the database.
    Returns inputaddress_list, outputaddress_list, and address_amt_map to be used to update and create new Wallet/Address entries in the database
    '''

    input_address_amt_map = {}
    output_address_amt_map = {}
    input_address_list = []
    output_address_list = []
    coinbase=False

    
    #Iterate through the input transactions in the transaction
    #Retreive the input transactions to get the addresses and amounts that are used as inputs
    for vin in transaction_dict['vin']:
        #If the transaction is not a coinbase (not the company!) transaction
        if 'coinbase' not in vin.keys():
            vin_tx_dict = json.loads(rpc.getTransactionbyTxid(vin['txid']))
            #Some (typcially) earlier transactions do not have an address input. This needs to be explored further.
            in_addr = vin_tx_dict['vout'][vin['vout']]['scriptPubKey']['addresses'][0] if 'addresses' in  vin_tx_dict['vout'][vin['vout']]['scriptPubKey'].keys() else None
            in_amt = vin_tx_dict['vout'][vin['vout']]['value']

            input_address_list.append(in_addr)
            input_address_amt_map[in_addr] = in_amt
        #If the transaction is a coinbase transaction
        else:
            coinbase=True

    #Iterate through outputs in the transaction
    for vout in transaction_dict['vout']:
        #Some (typcially) earlier transactions do not have an address output
        out_addr = vout['scriptPubKey']['addresses'][0] if 'addresses' in vout['scriptPubKey'].keys() else None
        out_amt = vout['value']

        output_address_list.append(out_addr)
        output_address_amt_map[out_addr] = out_amt

    if coinbase:
        netexchanged = transaction_dict['vout'][0]['value']
        fee = 0
    else:
        #Sum all of the currency exchanged within the particular transaction
        netexchanged = sum(input_address_amt_map.values()) + sum(output_address_amt_map.values())
        #The fee of any transaction is the input amounts minus the output amounts
        fee = sum(input_address_amt_map.values()) - sum(output_address_amt_map.values())
    
    block_model = Block.objects.get(pk=transaction_dict['blockhash'])

    transaction_model = Transaction(
        id= transaction_dict['txid'], 
        block= block_model, 
        coinbase= coinbase, 
        inputaddressmap= input_address_amt_map, 
        outputaddressmap= output_address_amt_map, 
        size= transaction_dict['size'], 
        timestamp= transaction_dict['time'], 
        netexchanged= netexchanged, 
        fee= fee,
        confirmations= transaction_dict['confirmations'], 
        json= transaction_dict
    )

    transaction_model.save(force_insert=True)

    return input_address_list, output_address_list, input_address_amt_map, output_address_amt_map

def updateAddressWithTransaction(address_str: str, txid_str: str, input_tx: bool, amt: float):

    address_model = Address.objects.get(pk=address_str)
    transaction_model = Transaction.objects.get(pk=txid_str)

    address_model.numtransactions += 1
    address_model.transactions.add(transaction_model)
    
    #WILL NEED TO REWRITE THIS TO USE SATOSHIS INSTEAD OF PYTHON FLOAT VALUES
    if input_tx:
        address_model.sent += amt
        address_model.balance -= amt
        address_model.tx_where_sent[txid_str] = amt #dont know if this will work
        address_model.transactionswhereinput.add(transaction_model)
        

    else:
        address_model.received += amt
        address_model.balance += amt
        address_model.tx_where_received[txid_str] = amt
        address_model.transactionswhereoutput.add(transaction_model)
    
    address_model.save() #not sure if this is needed

def createNewAddressEntry(address_str: str, txid_str: str, input_tx: bool, amt: float):
    '''
    Creates a new Address entry into the database
    Addresses should be on the receiving end of a transaction but not always.
    Special attention should be paid to the case where it is not on the receiving end. This means that a prior address/tx is missing from the database/blockchain.
    '''

    address_model = Address(
                        address = address_str,
                        received = amt,
                        sent = 0,
                        balance = amt,
                        numtransactions = 1,
                        tx_where_sent = {txid_str: amt} if input_tx else {},
                        tx_where_received = {txid_str: amt} if not input_tx else {}
                )

    address_model.save()

    #Now set the related fields within address
    transaction_model = Transaction.objects.get(pk=txid_str)

    if input_tx:
        address_model.transactionswhereinput.set([transaction_model])
    else:
        address_model.transactionswhereoutput.set([transaction_model])
    address_model.transactions.set([transaction_model])

def updateDatabaseByHeight(height: int):
    '''
    Update the database with data coming from a single block.
    Assuming this block is not already an entry in the database.
    '''

    if Block.objects.filter(height=height).exists():
        log.log('WARNING', 'database_update_service', 'Trying to create a new block entry when the block already exists in the database!')
        return

    #pdb.set_trace()
    block_dict = json.loads(rpc.getBlockByHeight(height))
    createNewBlockEntry(block_dict)

    #Iterate through all transactions in the block
    for txid in block_dict['tx']:
        transaction_dict = json.loads(rpc.getTransactionbyTxid(txid))

        input_address_list, output_address_list, input_address_amt_map, output_address_amt_map = \
        createNewTransactionEntry(transaction_dict)

        #Filter out any None values in the lists
        input_address_list = list(filter(None, input_address_list))
        output_address_list = list(filter(None, output_address_list))

        #Update/Add all Input Addresses in this transaction
        for address_str in input_address_list:
            if Address.objects.filter(pk=address_str).exists():
                updateAddressWithTransaction(address_str, txid, True, input_address_amt_map[address_str])
            else:
                log.log('WARNING', 'database_update_service', f'Input Address to transaction is not in the Database! TXID: {txid}, Address: {address_str}')
                createNewAddressEntry(address_str, txid, True, input_address_amt_map[address_str])
                
        #Update/Add all Output Addresses in this transaction
        for address_str in output_address_list:
            if Address.objects.filter(pk=address_str).exists():
                updateAddressWithTransaction(address_str, txid, False, output_address_amt_map[address_str])
            else:
                '''
                Create a new address entry in the Database
                Assuming that this address is not part of any block or transaction already contained in the chain.
                '''
                createNewAddressEntry(address_str, txid, False, output_address_amt_map[address_str])