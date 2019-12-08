import time
from datetime import datetime

import pytz
from django.db.models.aggregates import Count

from User.models import *
from games.models import Room


def get_leaderboard(user_id, room_id):
    room = Room.objects.get(id=room_id)
    user_ids = room.get_user_ids()

    now = datetime.fromtimestamp(time.time()).replace(tzinfo=pytz.UTC)
    user = User.objects.get(id=user_id)
    user_type = user.user_type.user_type

    if user_type == "delivery_partner":

        data = User.objects.filter(id__in=user_ids, partnerdeliveries__created_on__gte=room.start_time,
                                   partnerdeliveries__created_on__lte=now).annotate(
            total=Count('partnerdeliveries')).order_by(
            '-total')
    else:
        data = User.objects.filter(id__in=user_ids, partnerrides__created_on__gte=room.start_time,
                                   partnerrides__created_on__lte=now).annotate(
            total=Count('partnerrides')).order_by(
            '-total')
    data = [{'user_id': user_count['id'], 'total': user_count['total'], 'user_type': user_type} for user_count in
            data]

    leader_board_user_ids = [user_data['_id'] for user_data in data]
    user_ids_with_score_zero = list(set(user_ids) - set(leader_board_user_ids))
    data.extend([{'user_id': user_id, 'total': 0, 'user_type': user_type}] for user_id in user_ids_with_score_zero)
    return data
