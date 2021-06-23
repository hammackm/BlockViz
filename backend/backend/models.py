from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Block(models.Model):

    hash = models.CharField(max_length=64, primary_key=True)
    nexthash = models.CharField(max_length=64)
    prevhash = models.CharField(max_length=64)

    numtransactions = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    merkleroot = models.TextField()
    minedby = models.TextField()
    timestamp = models.DateTimeField()
    difficulty = models.FloatField()
    size = models.PositiveIntegerField()
    nonce = models.PositiveBigIntegerField()
    version = models.PositiveBigIntegerField()
    bits = models.PositiveBigIntegerField()
    netexchanged = models.FloatField()
    json = models.JSONField()

class Transaction(models.Model):

    id = models.TextField(primary_key=True)
    block = models.ForeignKey("Block", on_delete=models.SET_NULL, null=True)
    coinbase = models.BooleanField()
    inputtxids = models.ManyToManyField('Transaction', related_name="transactionswhereinput")
    inputaddresses = models.ManyToManyField('Address', related_name="transactionswhereinput")
    outputaddresses = models.ManyToManyField('Address', related_name="transactionswhereoutput")
    addressmap = models.JSONField()
    size = models.PositiveIntegerField()
    timestamp = models.DateTimeField()
    netexchanged = models.FloatField()
    confirmations = models.IntegerField()
    json = models.JSONField()

class Address(models.Model):
    address = models.TextField(primary_key=True)
    received = models.FloatField()
    send = models.FloatField()
    balance = models.FloatField()
    numtransactions = models.IntegerField()
    transactions = models.ManyToManyField('Transaction', related_name="addresses")
    json = models.JSONField()