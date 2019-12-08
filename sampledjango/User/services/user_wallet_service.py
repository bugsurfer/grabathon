from User.models import User, UserBalance


def get_user_balance(user_id):
    try:
        user = User.objects.get(id=user_id)
        user_balance = UserBalance.objects.get(user=user)
    except UserBalance.DoesNotExist:
        return None
    else:
        return user_balance.to_json()


def update_user_balance(user_id, transaction_amount, transaction_type, cash_type):
    balance = get_user_balance(user_id)
    if not balance:
        user = User.objects.get(id=user_id)
        UserBalance.objects.create(user=user)
        balance = get_user_balance(user_id)

    if cash_type == "cash":
        cash = balance.get('cash_amount')
        if transaction_type == "credit":
            cash = cash + transaction_amount
        else:
            cash = cash - transaction_amount
        UserBalance.objects.filter(user_id=user_id).update(cash=cash)
    elif cash_type == "rewards":
        rewards = balance.get('reward_amount')
        if transaction_type == "credit":
            rewards = rewards + transaction_amount
        else:
            rewards = rewards - transaction_amount
        UserBalance.objects.filter(user_id=user_id).update(rewards=rewards)


def check_minimum_reward_amount_available(amount, user_id):
    user_balance = get_user_balance(user_id)
    reward_amount = user_balance['reward_amount']
    if amount <= reward_amount:
        return True
    else:
        return False
