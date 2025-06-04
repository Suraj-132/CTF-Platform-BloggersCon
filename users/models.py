from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    PLAYER = 'player'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (PLAYER, 'Player'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=PLAYER)

    def __str__(self):
        return f"{self.username} ({self.role})"
