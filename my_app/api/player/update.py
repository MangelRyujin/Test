## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from typing import Any
from rest_framework.response import Response
from my_app.models.player import Player
from my_app.serializers.player import PlayerSerializer,UpdatePlayerSerializer

def update_player_handler(request: Request, id: Any):
    player = Player.objects.filter(id = id).first()
    if player:
            players_serializers = UpdatePlayerSerializer(player ,data = request.data)
            if players_serializers.is_valid():
                players_serializers.save()
                return Response(players_serializers.data, status = status.HTTP_200_OK)
            else:
                for e in players_serializers.errors.values():
                    error = e
                    break
                return Response(error, status= status.HTTP_400_BAD_REQUEST)
    return Response({"message':'Player don't exist!"},status = status.HTTP_400_BAD_REQUEST)
