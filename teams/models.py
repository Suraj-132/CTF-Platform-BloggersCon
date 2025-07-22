from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams', blank=True)
    captain = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='captained_teams',
        null=True, blank=True
    )
    description = models.TextField(blank=True, null=True)
    score = models.IntegerField(default=0)
    max_members = models.IntegerField(default=4)  # Maximum team size
    is_open = models.BooleanField(default=True)  # Open for joining
    invite_code = models.CharField(max_length=8, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.captain and self.captain not in self.members.all():
            raise ValidationError('Team captain must be a member of the team')

    def save(self, *args, **kwargs):
        # Generate invite code if not exists
        if not self.invite_code:
            import string
            import random
            self.invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)
        
        # Add captain as member if not already
        if self.captain:
            self.members.add(self.captain)

    @property
    def member_count(self):
        return self.members.count()

    @property
    def can_join(self):
        return self.is_open and self.member_count < self.max_members

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
    
   
