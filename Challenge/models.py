import uuid
import hashlib
from django.db import models
from django.conf import settings


#  Challenge Model 
def Challenge_file_upload_path(instance, filename):
    return f"Challenge/{instance.id}/{filename}"

class Challenge(models.Model):
    FLAG_TYPE_CHOICES = (
        ('static', 'Static'),
        ('regex', 'Regex'),
        ('plugin', 'Plugin'),
    )

    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')

    flag = models.CharField(max_length=255, help_text="Enter the correct flag (only stored temporarily)")
    flag_type = models.CharField(max_length=10, choices=FLAG_TYPE_CHOICES, default='static')
    flag_hash = models.CharField(max_length=65, editable=False)

    points = models.PositiveIntegerField(default=100)
    attachment = models.FileField(
        upload_to=Challenge_file_upload_path,
        null=True,
        blank=True,
        help_text="Optional file for the challenge (e.g., image, zip, doc)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.flag and not self.flag_hash:
            self.flag_hash = hashlib.sha256(self.flag.encode()).hexdigest()
            self.flag = ""  # Optionally clear the flag from DB
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.difficulty})"





#  Solve Model (individual) 
class Solve(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solves')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='solves')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.username} solved {self.challenge.title}"



