# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import models


# Create your models here.

class Games(models.Model):
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    min_players = models.IntegerField(default=0)
    max_players = models.IntegerField(default=0)
    target = models.IntegerField(default=0)
    category = models.CharField(max_length=256, default='')
    pitch_amount = models.IntegerField(default=0)
    start_time = models.DateTimeField()
    duration = models.IntegerField(default=0)  # in days
    user_type = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{}'.format(self.title)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'amount': self.pitch_amount,
            'duration': self.duration,
            'max_players': self.max_players,
            'start_time': self.start_time.strftime("%d %B, %Y %H:%M"),
            'category': self.category
        }


class Room(models.Model):
    game = models.ForeignKey(Games)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user_ids = models.CharField(max_length=2056)
    status = models.IntegerField(default=0)
    pool_amount = models.IntegerField(default=0)
    is_available = models.IntegerField(default=1)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{}'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'status': self.status,
            'pool_amount': self.pool_amount,
            'available': self.is_available,
            'user_ids': self.get_user_ids()
        }

    def get_user_ids(self):
        if not self.user_ids:
            return []
        return json.loads(self.user_ids)

    def append_user(self, user_id):
        user_ids = self.get_user_ids()
        user_ids.append(user_id)
        if len(user_ids) == self.game.max_players:
            self.is_available=0

            self.pool_amount = self.pool_amount + self.game.pitch_amount
        self.user_ids = json.dumps(user_ids)
        self.save()
