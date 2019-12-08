# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.http import JsonResponse

from games.models import Games, Room
from games.services.game_service import join_user_in_room, calculate_results


# Create your views here.

def get_games(request):
    user_type = request.GET.get('user_type', '')
    game_id = request.GET.get('game_id', '')
    if game_id:
        game_id = int(game_id)
        games = Games.objects.filter(game_id=game_id, user_type=user_type)
    else:
        games = Games.objects.filter(user_type=user_type)

    data = [game.to_json() for game in games]
    return JsonResponse({'code': 200, 'msg': 'success', 'data': data})


def join_game(request):
    game_id = int(request.GET.get('game_id'))
    user_id = int(request.GET.get('user_id'))

    game = Games.objects.get(id=game_id)
    return join_user_in_room(game_id, user_id, game.pitch_amount)


def start_game(request):
    room_id = int(request.GET.get('room_id'))

    room = st_game(room_id=room_id)
    return JsonResponse({'code': 200, 'msg': 'success', 'data': room.to_json()})


def st_game(room_id):
    room = Room.objects.get(id=room_id)
    game = room.game

    now = datetime.utcnow()
    room.start_time = now
    room.end_time = now + timedelta(days=game.duration)
    room.status = 1
    room.save()
    return room


def end_game(request):
    room_id = int(request.GET.get('room_id'))
    user_id = int(request.GET.get('user_id'))

    room = ed_game(room_id=room_id, user_id=user_id)
    return JsonResponse({'code': 200, 'msg': 'success', 'data': room.to_json()})


def ed_game(room_id, user_id):
    room = Room.objects.get(id=room_id)
    room.status = 2
    room.save()
    calculate_results(room_id, user_id)
    return room
