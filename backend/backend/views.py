from django.http import HttpResponse

from .vertcoin_node_rpc_service import NodeRPCService
from . import sanitization_utils
import pdb

rpc = NodeRPCService()

def getNMostRecentBlocks(request, unsafe_number):
    
    sanitized_number = sanitization_utils.number_input(unsafe_number)
    return HttpResponse(
        rpc.getNMostRecentBlocks(sanitized_number)
    )

def getNMostRecentTransactions(request, unsafe_number):

    sanitized_number = sanitization_utils.number_input(unsafe_number)
    return HttpResponse(
        rpc.getNMostRecentBlocks()
    )

def getBlockByHeight(request, unsafe_height):

    sanitized_height = sanitization_utils.number_input(unsafe_height)
    return HttpResponse(
        rpc.getBlockByHeight(sanitized_height)
    )

def getBlockByHash(request, unsafe_hash):

    sanitized_hash = sanitization_utils.hash_input(unsafe_hash)
    return HttpResponse(
        rpc.getBlockByHash(sanitized_hash)
    )

def getTransactionsByHeight(request, unsafe_height):

    sanitized_height = sanitization_utils.number_input(unsafe_height)
    return HttpResponse(
        rpc.getTransactionsByHeight(sanitized_height)
    )

def getTransactionbyTxid(request, unsafe_txid):

    sanitized_txid = sanitization_utils.hash_input(unsafe_txid)
    return HttpResponse(
        rpc.getTransactionbyTxid(sanitized_txid)
    )

def getMemPool(request):
    return HttpResponse(
        rpc.getMemPool()
    )