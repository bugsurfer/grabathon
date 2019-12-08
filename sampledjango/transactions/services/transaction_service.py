from django.db import transaction

from User.services.user_wallet_service import update_user_balance
from transactions.models import Transactions


def get_all_transactions(user_id):
    transactions = Transactions.objects.filter(user_id=user_id)
    data = [transaction.to_json() for transaction in transactions]
    return data


def get_transaction_details(transaction_id):
    try:
        transaction = Transactions.objects.get(id=transaction_id)
    except Transactions.DoesNotExist:
        return None
    else:
        return transaction.to_json()


def create_transaction(user_id, transaction_amount, transaction_type, cash_type, transaction_from=0):
    with transaction.atomic():
        Transactions.objects.create(user_id=user_id, transaction_amount=transaction_amount,
                                    transaction_type=transaction_type, cash_type=cash_type,
                                    transaction_from_user_id=transaction_from)
        update_user_balance(user_id, transaction_amount, transaction_type, cash_type)
