## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from my_app.serializers.player import PlayerSerializer



def create_player_handler(request: Request):
    if request.data.__contains__('playerSkills') and request.data['playerSkills'] != [] :  
        players_serializers = PlayerSerializer(data = request.data,context = request.data['playerSkills'] )
        if players_serializers.is_valid():
            players_serializers.save()
            return Response(players_serializers.data, status=status.HTTP_201_CREATED)
        else:
            for e in players_serializers.errors.values():
                error = e
                break
        return Response(error, status= status.HTTP_400_BAD_REQUEST)
    return Response({'message':'The player must contain at least one skill'}, status= status.HTTP_400_BAD_REQUEST)
    
