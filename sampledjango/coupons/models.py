# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class Coupons(models.Model):
    coupon_type = models.CharField(max_length=256, null=False, blank=False)
    discount_type = models.CharField(max_length=256, null=False, blank=False)
    discount = models.IntegerField(default=0)
    code = models.CharField(max_length=256, null=False, blank=False, unique=True)
    description = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'{}-{}'.format(self.code, self.coupon_type)

    def to_json(self):
        return {
            'code': self.code,
            'discount': self.discount,
            'discount_type': self.discount_type,
            'coupon_type': self.coupon_type,
            'description': self.description
        }


class UserCoupons(models.Model):
    user_id = models.CharField(max_length=256, null=False, blank=False)
    coupon = models.ForeignKey(Coupons)

    def __unicode__(self):
        return u'{}-{}'.format(self.user_id, self.coupon)

    def to_json(self):
        return {
            'coupon_details': self.coupon.to_json()
        }
