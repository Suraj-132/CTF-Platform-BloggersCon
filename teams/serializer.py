# teams/serializers.py
from rest_framework import serializers
from .models import Team

class TeamLeaderboardSerializer(serializers.ModelSerializer):
    rank = serializers.IntegerField()
    last_solve = serializers.DateTimeField()
    members = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['rank', 'team_name', 'score', 'last_solve', 'members']

    def get_members(self, obj):
        return [member.username for member in obj.members.all()]