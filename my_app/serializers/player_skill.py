from rest_framework import serializers

from my_app.models.player import Player
from ..models.player_skill import PlayerSkill

class PlayerSkillSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = PlayerSkill
        fields = ['id', 'skill', 'value','player']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'skill' : instance.skill,
            'value' : instance.value,
            'playerId' : instance.player.id,
        }
        
    
    # Method validate skills in the request    
    def validate_skill(self,value):
        skills = ['defense','attack','speed','strength','stamina']
        if value in skills:
            return value
        else:
            raise serializers.ValidationError({'message':f'invalid value for skill: {value}'})
    
    # Method validate value in the request     
    def validate_value(self,value):
        value_str = str(value)
        if value_str.isdigit():
            return value
        else:
            raise serializers.ValidationError({'message':f'invalid value for value: {value}'})
    
    # Method validate player exist   
    def validate_player(self,value):
        player = Player.objects.filter(id = value.id).first()
        if player:
            return value
        else:
            raise serializers.ValidationError({'message':f'invalid value for player: {value.id}'})
    
class UpdatePlayerSkillSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = PlayerSkill
        fields = ['id', 'skill', 'value','player']
        extra_kwargs = {'id': {'read_only':False},'player':{'read_only':True}}
        
    # Method validate skills in the request    
    def validate_skill(self,value):
        skills = ['defense','attack','speed','strength','stamina']
        if value in skills:
            return value
        else:
            raise serializers.ValidationError({'message':f'invalid value for skill: {value}'})
    
    # Method validate value in the request     
    def validate_value(self,value):
        value_str = str(value)
        if value_str.isdigit():
            return value
        else:
            raise serializers.ValidationError({'message':f'invalid value for value: {value}'})
    
class SelectionPlayerSkillSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = PlayerSkill
        fields = ['skill', 'value']

    def to_representation(self, instance):
        return {
            'skill' : instance.skill,
            'value' : instance.value,
            
        }