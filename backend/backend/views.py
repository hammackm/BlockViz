from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from . import vertcoin_node_rpc_service as rpc

from .models import Block, Transaction, Address

# Create your views here.
def getNMostRecentBlocks(request, number):
    return HttpResponse(rpc.getNMostRecentBlocks(number))

def getNMostRecentTransactions(request, number):
    return HttpResponse(
        rpc.getNMostRecentBlocks()
    )

def getBlockByHeight(request, height):
    return HttpResponse(
        rpc.getBlockByHeight(height)
    )

def getBlockByHash(request, hash):
    return HttpResponse(
        rpc.getBlockByHash(hash)
    )

def getTransactionsByHeight(request, height):
    return HttpResponse(
        rpc.getTransactionsByHeight(height)
    )

def getTransactionbyTxid(request, txid):
    return HttpResponse(
        rpc.getTransactionbyTxid(txid)
    )

def getMemPool(request):
    return HttpResponse(
        rpc.getMemPool()
    )