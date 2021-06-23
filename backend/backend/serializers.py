from rest_framework import serializers

from .models import Block, Transaction, Address

class BlockSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Block
        fields = ('hash',
                'nexthash',
                'prevhash',
                'numtransactions',
                'height',
                'merkleroot',
                'minedby',
                'timestamp',
                'difficulty',
                'size',
                'nonce',
                'version',
                'bits',
                'netexchanged',
                'json')

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id',
                'block',
                'coinbase',
                'inputtxids',
                'inputaddresses',
                'outputaddresses',
                'addressmap',
                'size',
                'timestamp',
                'netexchanged',
                'confirmations',
                'json')

class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('address',
                'received',
                'send',
                'balance',
                'numtransactions',
                'transactions',
                'json')