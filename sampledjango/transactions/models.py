# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Transactions(models.Model):
    user_id = models.IntegerField(null=False, blank=False)
    transaction_from_user_id = models.IntegerField(default=0)
    transaction_amount = models.IntegerField(default=0)
    transaction_type = models.CharField(max_length=256)  # credit or debit
    cash_type = models.CharField(max_length=256)  # cash or rewards
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{}-{}-{}'.format(self.user_id, self.transaction_amount, self.transaction_type)

    def to_json(self):
        return {
            'id': self.id,
            'transaction_amount': self.transaction_amount,
            'transaction_type': self.transaction_type,
            'created_on': self.created_on.strftime("%d %B, %Y %H:%M")
        }
