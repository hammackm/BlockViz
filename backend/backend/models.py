from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Chain(models.Model):

    latestdbblockheight = models.BigIntegerField()

class Block(models.Model):

    hash = models.CharField(max_length=64, primary_key=True)
    nexthash = models.CharField(max_length=64, null=True)
    prevhash = models.CharField(max_length=64, null=True)

    numtransactions = models.PositiveIntegerField(null=True)
    confirmations = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    merkleroot = models.TextField(null=True)
    minedby = models.TextField(null=True)
    timestamp = models.DateTimeField(null=True)
    difficulty = models.FloatField(null=True)
    size = models.PositiveIntegerField(null=True)
    nonce = models.PositiveBigIntegerField(null=True)
    version = models.PositiveBigIntegerField(null=True)
    bits = models.TextField(null=True)
    netexchanged = models.FloatField(null=True)
    json = models.JSONField(null=True)

class Transaction(models.Model):

    id = models.TextField(primary_key=True)
    block = models.ForeignKey("Block", on_delete=models.SET_NULL, null=True, related_name='transactions')
    coinbase = models.BooleanField(null=True)
    inputaddresses = models.ManyToManyField('Address', related_name="transactionswhereinput")
    outputaddresses = models.ManyToManyField('Address', related_name="transactionswhereoutput")
    inputaddressmap = models.JSONField(null=True)
    outputaddressmap = models.JSONField(null=True)
    size = models.PositiveIntegerField(null=True)
    timestamp = models.DateTimeField(null=True)
    netexchanged = models.FloatField(null=True)
    fee = models.FloatField(null=True)
    confirmations = models.PositiveIntegerField(null=True)
    json = models.JSONField(null=True)

class Address(models.Model):
    address = models.TextField(primary_key=True)
    received = models.FloatField(null=True)
    sent = models.FloatField(null=True)
    balance = models.FloatField(null=True)
    numtransactions = models.IntegerField(null=True)
    transactions = ArrayField(models.TextField(null=True), null=True)
    tx_where_sent = models.JSONField(null=True)
    tx_where_received = models.JSONField(null=True)