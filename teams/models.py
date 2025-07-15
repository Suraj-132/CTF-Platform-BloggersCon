from django.db import models
from django.conf import settings

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams')
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class TeamSolve(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_solves')
    challenge = models.ForeignKey('Challenge.Challenge', on_delete=models.CASCADE, related_name='team_solves')  # ✅ fixed
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'challenge')

    def __str__(self):
        return f"{self.team.name} team solved {self.challenge.title}"
    
   
