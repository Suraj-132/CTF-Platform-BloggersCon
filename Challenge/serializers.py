from rest_framework import serializers
from .models import Challenge, Solve
from teams.models import TeamSolve
import hashlib

# ✅ Challenge Serializer (used in views to list/detail challenges)
class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


# ✅ Used for flag submission
class FlagSubmissionSerializer(serializers.Serializer):
    flag = serializers.CharField()

    def validate(self, data):
        challenge = self.context['challenge']
        user = self.context['request'].user
        submitted_flag = data['flag'].strip()
        submitted_hash = hashlib.sha256(submitted_flag.encode()).hexdigest()

        #  Incorrect flag
        if submitted_hash != challenge.flag_hash:
            raise serializers.ValidationError("Incorrect flag.")

        #  Already solved
        if Solve.objects.filter(user=user, challenge=challenge).exists():
            raise serializers.ValidationError("You have already solved this challenge.")

        return data

    def save(self, **kwargs):
        challenge = self.context['challenge']
        user = self.context['request'].user
        team = user.teams.first()

        #  Record individual solve
        Solve.objects.create(user=user, challenge=challenge)
        user.score += challenge.points
        user.save()

        #  Record team solve if not already
        if team and not TeamSolve.objects.filter(team=team, challenge=challenge).exists():
            TeamSolve.objects.create(team=team, challenge=challenge)
            team.score += challenge.points
            team.save()
