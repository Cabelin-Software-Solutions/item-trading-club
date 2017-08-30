# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name="owned_items",null=True)
    in_sender_trade = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now    =True)

class Proposal(models.Model):
    status = models.CharField(max_length=255)
    sender = models.ForeignKey(User, related_name = "send_proposals")
    receiver = models.ForeignKey(User, related_name = "receive_proposals")
    sender_item = models.ForeignKey(Item, related_name = "item_send_proposals",null=True,blank=True)
    receiver_item = models.ForeignKey(Item, related_name = "item_receive_proposals",null=True,blank=True)
    is_finalized = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now    =True)

class Log(models.Model):
    message = models.CharField(max_length=255)
    trade = models.OneToOneField(Proposal, related_name="log_message")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now    =True)