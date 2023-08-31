## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from my_app.models.player import Player
from my_app.serializers.player import PlayerSerializer
from rest_framework.response import Response


def get_player_list_handler(request: Request):
    players = Player.objects.all()
    if players.exists():
        players_serializers = PlayerSerializer(players,many = True)
        return Response(players_serializers.data, status = status.HTTP_200_OK)
    return Response({'message':"Players don't exists"}, status = status.HTTP_200_OK)