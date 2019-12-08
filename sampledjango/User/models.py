# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class UserType(models.Model):
    user_type = models.CharField(max_length=256, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{}'.format(self.user_type)

    def to_json(self):
        return {
            'id': self.id,
            'user_type': self.user_type,
        }


class User(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256, default='')
    user_type = models.ForeignKey(UserType)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{}-{}'.format(self.email, self.user_type.user_type)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.get_user_name(),
            'email': self.email
        }

    def get_user_name(self):
        return self.first_name + ' ' + self.last_name


class UserBalance(models.Model):
    user = models.ForeignKey(User)
    cash = models.IntegerField(default=0)
    rewards = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{}-{}-{}'.format(self.user, self.cash, self.rewards)

    def to_json(self):
        return {
            'user_name': self.user.get_user_name(),
            'email': self.user.email,
            'cash_amount': self.cash,
            'reward_amount': self.rewards,
            'total_amount': self.get_total_balance()
        }

    def get_total_balance(self):
        return self.cash + self.rewards


class PartnerRides(models.Model):
    user = models.ForeignKey(User)
    ride_id = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{}-{}'.format(self.user, self.ride_id)

    def to_json(self):
        return {}


class PartnerDeliveries(models.Model):
    user = models.ForeignKey(User)
    delivery_id = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{}-{}'.format(self.user, self.delivery_id)

    def to_json(self):
        return {}
