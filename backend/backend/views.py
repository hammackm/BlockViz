from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from . import cli

from .models import Block, Transaction, Address

# Create your views here.
def getNMostRecentBlocks(request, number):
    return HttpResponse(cli.getNMostRecentBlocks(number))

def getNMostRecentTransactions(request, number):
    return HttpResponse(
        cli.getNMostRecentBlocks()
    )

def getBlockByHeight(request, height):
    return HttpResponse(
        cli.getBlockByHeight(height)
    )

def getBlockByHash(request, hash):
    return HttpResponse(
        cli.getBlockByHash(hash)
    )

def getTransactionsByHeight(request, height):
    return HttpResponse(
        cli.getTransactionsByHeight(height)
    )

def getTransactionbyTxid(request, txid):
    return HttpResponse(
        cli.getTransactionbyTxid(txid)
    )

def getMemPool(request):
    return HttpResponse(
        cli.getMemPool()
    )