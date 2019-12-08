# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse

from coupons.models import Coupons, UserCoupons


# Create your views here.

def get_coupons(request):
    user_id = int(request.GET.get('user_id'))
    codes = get_user_coupon_codes(user_id)
    try:
        coupons = list(Coupons.objects.exclude(codes__in=codes))
        data = [coupon.to_json() for coupon in coupons]
        return JsonResponse({'code': 200, 'msg': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'Something Went Wrong!'})


def reedem_coupon(request):
    coupon_id = int(request.GET.get('coupon_id'))
    user_id = int(request.GET.get('coupon_id'))

    try:
        coupon = Coupons.objects.get(id=coupon_id)
    except Coupons.DoesNotExist:
        return JsonResponse({'code': 401, 'msg': 'Invalid Coupon!'})
    else:
        UserCoupons.objects.create(user_id=user_id, coupon=coupon)
        return JsonResponse({'code': 200, 'msg': 'Successfully Redeemed'})


def user_coupons(request):
    user_id = int(request.GET.get('coupon_id'))
    coupon_type = (request.GET.get('coupon_type'))
    data = get_user_coupons(user_id, coupon_type)
    return JsonResponse({'code': 200, 'msg': 'Success', data: data})


def get_user_coupons(user_id, coupon_type):
    return [user_coupon.to_json for user_coupon in
            list(UserCoupons.objects.filter(user_id=user_id, coupon__coupon_type=coupon_type))]


def get_user_coupon_codes(user_id):
    data = get_user_coupons(user_id)
    coupon_details = data['coupon_details']
    codes = [coupon['code'] for coupon in coupon_details]
    return codes


def create_coupon(request):
    import ipdb
    ipdb.set_trace()
    code = (request.GET.get('code'))
    discount = int(request.GET.get('discount'))
    discount_type = (request.GET.get('discount_type'))
    description = (request.GET.get('description'))
    coupon_type = (request.GET.get('coupon_type'))

    coupon = Coupons.objects.create(code=code, discount=discount, discount_type=discount_type, description=description,
                                    coupon_type=coupon_type)
    return JsonResponse({'code': 200, 'msg': 'Success', 'data': coupon.to_json()})
