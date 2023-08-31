## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from typing import Any
from rest_framework.response import Response
from my_app.models.player import Player




def delete_player_handler(request: Request, id: Any):
    data= request.data
    if data.__contains__('headers') and data.get('headers') != {}:
        token = data.__getitem__('headers').get('Authorization')
        if token == "Bearer SkFabTZibXE1aE14ckpQUUxHc2dnQ2RzdlFRTTM2NFE2cGI4d3RQNjZmdEFITmdBQkE=":
            player = Player.objects.filter(id = id).first()
            if player:
                player.delete()
                return Response({'message':'Eliminated player'},status=status.HTTP_200_OK)
            else:
                return Response({'message':"Player don't exist"},status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':"You don't have authorization to delete."},status=status.HTTP_401_UNAUTHORIZED)