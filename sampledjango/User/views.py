# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from models import UserType, User, PartnerRides, PartnerDeliveries, UserBalance
from services.leader_board_service import get_leaderboard
from services.user_wallet_service import get_user_balance


@csrf_exempt
def user(request):
    # import ipdb
    # ipdb.set_trace()
    if request.method == "GET":
        return get_user_details(request)
    elif request.method == "POST":
        return create_user(request)
    else:
        return JsonResponse("Invalid Request")


def create_user(request):
    body = json.loads(request.body)
    first_name = body.get('first_name', '')
    last_name = body.get('last_name', '')
    user_type = body.get('user_type')
    email = body.get('email')

    try:
        user_type_obj = UserType.objects.get(user_type=user_type)

    except UserType.DoesNotExist:
        return JsonResponse({'code': 404, 'msg': "User Type is Invalid"})

    try:
        user = User.objects.create(first_name=first_name, last_name=last_name, user_type=user_type_obj, email=email)
        UserBalance.objects. create(user=user, rewards=800)
    except Exception as e:
        return JsonResponse({"Error in creating User"})
    else:

        return JsonResponse({'code': 200, 'msg': 'success', 'data': user.to_json()})


def get_user_details(request):
    user_id = int(request.GET.get('user_id'))
    user_id = int(request.GET.get('user_id'))
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'code': 404, 'msg': 'Invalid User'})
    else:
        return JsonResponse({'code': 200, 'msg': 'success', 'data': user.to_json()})


def get_balance(request):
    user_id = int(request.GET.get('user_id'))
    # import ipdb
    # ipdb.set_trace()
    data = get_user_balance(user_id)
    if not data:
        return JsonResponse({'code': 404, 'msg': 'Invalid User'})

    return JsonResponse({'code': 200, 'msg': 'success', 'data': data})


def ride_complete(request):
    user_id = int(request.GET.get('user_id'))
    ride_id = int(request.GET.get('ride_id'))

    user = User.objects.get(id=user_id)
    partner_ride = PartnerRides.objects.create(user=user, ride_id=ride_id)
    return JsonResponse({'code': 200, 'msg': 'success', 'data': partner_ride.to_json()})


def delivery_complete(request):
    # import ipdb
    # ipdb.set_trace()
    user_id = int(request.GET.get('user_id'))
    delivery_id = int(request.GET.get('delivery_id'))
    try:
        user = User.objects.get(id=user_id)
        partner_delivery = PartnerDeliveries.objects.create(user=user, delivery_id=delivery_id)
    except Exception as e:
        print e
    return JsonResponse({'code': 200, 'msg': 'success', 'data': partner_delivery.to_json()})


def leaderboard(request):
    room_id = int(request.GET.get('room_id'))
    user_id = int(request.GET.get('user_id'))
    data = get_leaderboard(user_id, room_id)

    return JsonResponse({'code': 200, 'msg': 'success', 'data': data})
