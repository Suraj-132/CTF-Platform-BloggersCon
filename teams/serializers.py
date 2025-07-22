# teams/serializers.py
from rest_framework import serializers
from .models import Team
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'score']

class TeamSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True, read_only=True)
    captain = TeamMemberSerializer(read_only=True)
    member_count = serializers.ReadOnlyField()
    can_join = serializers.ReadOnlyField()
    invite_code = serializers.CharField(read_only=True)
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'captain', 'members', 'score', 
            'member_count', 'max_members', 'is_open', 'can_join', 
            'invite_code', 'created_at', 'updated_at'
        ]
        read_only_fields = ['score', 'created_at', 'updated_at']

class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description', 'max_members', 'is_open']
    
    def validate_name(self, value):
        if Team.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A team with this name already exists.")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        # Check if user is already in a team (optional - remove if multiple teams allowed)
        if user.teams.exists():
            raise serializers.ValidationError("You are already a member of a team.")
        
        team = Team.objects.create(
            captain=user,
            **validated_data
        )
        return team

class TeamJoinSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=8)
    
    def validate_invite_code(self, value):
        try:
            team = Team.objects.get(invite_code=value.upper())
        except Team.DoesNotExist:
            raise serializers.ValidationError("Invalid invite code.")
        
        user = self.context['request'].user
        
        # Check if user is already in a team (optional - remove if multiple teams allowed)
        if user.teams.exists():
            raise serializers.ValidationError("You are already a member of a team.")
        
        if not team.can_join:
            raise serializers.ValidationError("This team is full or not accepting new members.")
        
        self.team = team
        return value
    
    def save(self):
        user = self.context['request'].user
        self.team.members.add(user)
        return self.team

class TeamLeaderboardSerializer(serializers.ModelSerializer):
    rank = serializers.IntegerField()
    last_solve = serializers.DateTimeField()
    members = serializers.SerializerMethodField()
    captain_name = serializers.CharField(source='captain.username', read_only=True)

    class Meta:
        model = Team
        fields = ['rank', 'name', 'score', 'last_solve', 'members', 'captain_name', 'member_count']

    def get_members(self, obj):
        return [member.username for member in obj.members.all()]

class TeamUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', 'description', 'max_members', 'is_open']
    
    def validate_name(self, value):
        # Allow same name for current team, but not for others
        if Team.objects.filter(name__iexact=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("A team with this name already exists.")
        return value
    
    def validate(self, data):
        team = self.instance
        if 'max_members' in data and data['max_members'] < team.member_count:
            raise serializers.ValidationError({
                'max_members': 'Cannot set max members below current member count.'
            })
        return data

class TeamLeaveSerializer(serializers.Serializer):
    def validate(self, data):
        user = self.context['request'].user
        team = self.context['team']
        
        if user not in team.members.all():
            raise serializers.ValidationError("You are not a member of this team.")
        
        if user == team.captain and team.member_count > 1:
            raise serializers.ValidationError(
                "Captain cannot leave team with other members. Transfer captaincy first."
            )
        
        return data
    
    def save(self):
        user = self.context['request'].user
        team = self.context['team']
        
        team.members.remove(user)
        
        # If captain leaves and no other members, delete team
        if user == team.captain and team.member_count == 0:
            team.delete()
            return None
        
        return team
