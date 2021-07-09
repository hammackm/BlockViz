from django.urls import path

from . import views

urlpatterns = [
    # was having issues with int:height
    path('recent/block/<int:unsafe_number>', views.getNMostRecentBlocks, name='NMostRecentBlocks'),
    path('recent/transaction/<str:unsafe_number>', views.getNMostRecentTransactions, name='NMostRecentTransactions'),
    path('height/<str:unsafe_height>', views.getBlockByHeight, name='BlockByHeight'),
    path('blockhash/<str:unsafe_hash>', views.getBlockByHash, name='BlockByHash'),
    path('transactions/<str:unsafe_height>', views.getTransactionsByHeight, name='TransactionsByHeight'),
    path('transaction/<str:unsafe_txid>', views.getTransactionbyTxid, name='TransactionByTxid'),
    path('mempool/', views.getMemPool, name='MemPool')
]