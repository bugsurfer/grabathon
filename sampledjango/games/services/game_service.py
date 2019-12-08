from datetime import timedelta

from django.http import JsonResponse

from User.services.leader_board_service import get_leaderboard
from User.services.user_wallet_service import check_minimum_reward_amount_available, update_user_balance
from games.models import Games, Room


def join_user_in_room(game_id, user_id, amount):
    if not check_minimum_reward_amount_available(amount, user_id):
        return JsonResponse({'code': 400, 'msg': 'Your CashBack Amount is not sufficient to Join the Game'})

    rooms = get_available_rooms(game_id)
    # import ipdb
    # ipdb.set_trace()
    if rooms:
        room = rooms[0]
        user_ids = room.get_user_ids()
        if room.is_available:
            room.append_user(user_id=user_id)
            update_user_balance(user_id=user_id, transaction_amount=amount, transaction_type="debit",
                                cash_type="rewards")
            return JsonResponse({'code': 200, 'msg': 'success', 'data': room.to_json()})

    game = Games.objects.get(id=game_id)
    Room.objects.create(game=game, start_time=game.start_time, end_time=game.start_time + timedelta(days=2))
    return join_user_in_room(game_id, user_id, amount)


def get_available_rooms(game_id):
    return list(Room.objects.filter(game_id=game_id, status=0, is_available=1))


def calculate_results(room_id, user_id):
    room = Room.objects.get(id=room_id)
    game = room.game
    total_pooled_amount = room.pool_amount
    data = get_leaderboard(user_id=user_id, room_id=room_id)

    limit_crossed = []
    for x in data:
        if x['total'] > game.target:
            limit_crossed.append(x)

    if not limit_crossed:
        return
    user_ids = [x['user_id'] for x in limit_crossed]
    if are_all_players_equal(limit_crossed):
        amount = int(total_pooled_amount / len(user_ids))
        for user_id in user_ids:
            update_user_balance(user_id=user_id, transaction_amount=amount, transaction_type="credit",
                                cash_type="rewards")
    else:
        if len(user_ids) == 2:
            amounts = [0.7 * total_pooled_amount, 0.3 * total_pooled_amount]
        else:
            amounts = [0.5 * total_pooled_amount, 0.3 * total_pooled_amount, 0.2 * total_pooled_amount]

        for i in range(0, len(user_ids)):
            user_id = user_ids[i]
            amount = amounts[i]
            update_user_balance(user_id=user_id, transaction_amount=amount, transaction_type="credit",
                                cash_type="rewards")


def are_all_players_equal(self, data):
    data[:] = data
    data = [x.pop('user_id') for x in data]
    data = list(set(data))
    if len(data) == 1:
        return True
    else:
        return False
