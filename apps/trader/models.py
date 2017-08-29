# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name="owned_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now    =True)

class Proposal(models.Model):
    status = models.CharField(max_length=255)
    sender = models.ForeignKey(User, related_name = "sent_proposals")
    receiver = models.ForeignKey(User, related_name = "received_proposals")
    sender_item = models.OneToOneField(Item, related_name = "item_sender_proposal")
    receiver_item = models.OneToOneField(Item, related_name = "item_receiver_proposal")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now    =True)