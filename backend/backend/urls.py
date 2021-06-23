from django.urls import path

from . import views

urlpatterns = [
    # ex: /backend/
    path('recent/block/<int:number>', views.getNMostRecentBlocks, name='NMostRecentBlocks'),
    path('recent/transaction/<str:number>', views.getNMostRecentTransactions, name='NMostRecentTransactions'),
    path('height/<str:height>', views.getBlockByHeight, name='BlockByHeight'),
    path('blockhash/<str:hash>', views.getBlockByHash, name='BlockByHash'),
    path('transactions/<str:height>', views.getTransactionsByHeight, name='TransactionsByHeight'),
    path('transaction/<str:txid>', views.getTransactionbyTxid, name='TransactionByTxid'),
    path('mempool/', views.getMemPool, name='MemPool')
]