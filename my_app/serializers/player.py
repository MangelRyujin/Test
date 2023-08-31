from rest_framework import serializers 
from my_app.models.player_skill import PlayerSkill
from .player_skill import PlayerSkillSerializer,SelectionPlayerSkillSerializer,UpdatePlayerSkillSerializer
from ..models.player import Player
import re

class PlayerSerializer(serializers.ModelSerializer):
    playerSkills = PlayerSkillSerializer(many = True, read_only=True)

    class Meta:
        model = Player
        fields = ['id','name','position','playerSkills']
        
    # Validate value position in the request  
    def validate_position(self,value):
        positions = ['defender','midfielder','forward']
        if value in positions:
            return value
        else:
            raise serializers.ValidationError({'message':f'invalid value for position: {value}'})
        
    # Validate value name in the request
    def validate_name(self,value):
        if re.fullmatch(r"[A-Za-z ]{1,64}",value):
            return value
        else:
            raise serializers.ValidationError({'message':f'invalid value for name: {value}'})
        
    
    # Method create the PlayerSerializer   
    def create(self,validated_data):
        instance = Player.objects.create(
            name = validated_data['name'],
            position = validated_data['position']
        )
        self.create_skills(instance)  
        return instance
            
    # Method for create the skills in the PlayerSerializer
    def create_skills(self,player):
        new_context = []
        for skill in self.context:
            skill_add = {
                'skill': skill['skill'],
                'value': skill['value'],
                'player': player.id
            }
            new_context.append(skill_add)
        skills_serializers = PlayerSkillSerializer(data=new_context,many = True)
        if skills_serializers.is_valid():
            skills_serializers.save()
        else:
            for e in skills_serializers.errors:
                error = e
                break
            player = Player.objects.filter(id = player.id).first()
            player.delete()
            raise serializers.ValidationError(error)
        
    # Method update the PlayerSerializer   
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.position = validated_data.get('position',instance.position)
        instance.save()
        return instance    
    
class UpdatePlayerSerializer(serializers.ModelSerializer):
    playerSkills = UpdatePlayerSkillSerializer(many = True)

    class Meta:
        model = Player
        fields = ['id','name','position','playerSkills']
    
    # Validate value position in the request  
    def validate_position(self,value):
        positions = ['defender','midfielder','forward']
        if value in positions:
            return value
        else:
            raise serializers.ValidationError({'message':f'invalid value for position: {value}'})
        
    # Validate value name in the request
    def validate_name(self,value):
        if re.fullmatch(r"[A-Za-z ]{1,64}",value):
            return value
        else:
            raise serializers.ValidationError({'message':f'invalid value for name: {value}'})
    
    def update(self, instance, validated_data):
        skills_data = validated_data.pop('playerSkills')
        instance.name = validated_data.get('name',instance.name)
        instance.position = validated_data.get('position',instance.position)
        instance.save()
        for skill in skills_data:
            player_skill = PlayerSkill.objects.filter(id = skill.get('id')).first()
            if player_skill:
                player_skill.skill = skill.get('skill')
                player_skill.value = skill.get('value')
                player_skill.save()
        return instance 
        
class SelectionPlayerSerializer(serializers.ModelSerializer):
    playerSkills = SelectionPlayerSkillSerializer(many = True)
    
    class Meta:
        model = Player
        fields = ['name','position','playerSkills']
        