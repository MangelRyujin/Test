## /////////////////////////////////////////////////////////////////////////////
## YOU CAN FREELY MODIFY THE CODE BELOW IN ORDER TO COMPLETE THE TASK
## /////////////////////////////////////////////////////////////////////////////

from django.http.response import JsonResponse
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from my_app.models.player import Player
from my_app.models.player_skill import PlayerSkill
from my_app.serializers.player import SelectionPlayerSerializer


def team_process_handler(request: Request):
    selection = request.data
    if repeat_request(selection):
        best_equip,message = select(selection)
        if message != '':
            return Response({'message':message} ,status = status.HTTP_400_BAD_REQUEST)
        else:
            players_serializers = SelectionPlayerSerializer(best_equip,many = True)
            return Response(players_serializers.data, status = status.HTTP_200_OK)
    else:
        return Response({'message':"Don't repeat the request"}, status = status.HTTP_400_BAD_REQUEST)
     
# Method to select the players of the best team returns the team and a message
def select(selection):
    equipo = []
    message = ''
    for select in selection:
        mayor = -1
        mayor_skill = PlayerSkill
        cont= select.get('numberOfPlayers')
        players = Player.objects.filter(position = select.get('position'))
        if len(players) >= cont:
            while cont>0:
                for player in players:
                    if in_team(equipo,player) != 0:
                        skills = PlayerSkill.objects.filter(player = player.id, skill = select.get('mainSkill'))
                        for skill in skills:
                            if skill.value > mayor:
                                mayor = skill.value
                                mayor_skill = skill
                if mayor == -1:
                    for player in players:
                        if in_team(equipo,player) != 0:
                            skills = PlayerSkill.objects.filter(player = player.id)
                            for skill in skills:
                                if skill.value > mayor:
                                    mayor = skill.value
                                    mayor_skill = skill
                equipo.append(Player.objects.filter(id = mayor_skill.player.id).first())
                cont=cont-1
                mayor=-1
        else:
            message = f"Número insuficiente de jugadores para la posición: {select.get('position')}"
    return equipo,message
        
# Method to check if the player is in the team    
def in_team(team,player):
    if player in team:
        return 0
    else: 
        return 1
    
#  Method to go through the requests and check them
def repeat_request(selection):
    request = []
    for select in selection:
        position = Reapet(select.get('position'),select.get('mainSkill'))
        if in_request(request,select) ==0:
            return False    
        request.append(position)
    return True
        
# Method to check if requests are repeated
def in_request(request,selection):
    for select in request:
        if select.position == selection.get('position') and select.mainSkill == selection.get('mainSkill') :
            return 0
    return 1

# Class to instantiate the request
class Reapet():
    
    def __init__(self,position,mainSkill) -> None:
        self.position = position
        self.mainSkill = mainSkill
        
    def __str__(self) -> str:
        return f'{self.position} {self.mainSkill}'

