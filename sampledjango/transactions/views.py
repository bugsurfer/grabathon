# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from User.services.user_wallet_service import get_user_balance
from transactions.services.transaction_service import get_all_transactions, get_transaction_details, create_transaction


# Create your views here.

def get_all_transaction(request):
    transaction_id = request.GET.get('transaction_id', '')
    user_id = int(request.GET.get('user_id', ''))

    try:
        if not transaction_id:
            data = get_all_transactions(user_id)
            return JsonResponse({'code': 200, 'msg': 'success', 'data': data})
        transaction_id = int(transaction_id)
        data = get_transaction_details(transaction_id)
        if not data:
            return JsonResponse({'code': 404, 'msg': 'Invalid Request'})
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': 'Something Went Wrong!'})


@csrf_exempt
def add_cash(request):
    body = json.loads(request.body)
    user_id = int(body.get('user_id'))
    transaction_amount = int(body.get('amount'))

    create_transaction(user_id=user_id, transaction_amount=transaction_amount, transaction_type="credit",
                       cash_type="cash")

    data = get_user_balance(user_id=user_id)
    return JsonResponse({'code': 200, 'msg': 'success', 'data': data})
