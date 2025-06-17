import uuid
from django.db import models

def Challenge_file_upload_path(instance, filename):
    # Files will be stored as: media/challenges/<uuid>/<filename>
    return f"Challenge/{instance.id}/{filename}"


class Challenge(models.Model):
    FLAG_TYPE_CHOICES = (
        ('static', 'Static'),   # Exact match flag
        ('regex', 'Regex'),     # Regular expression pattern
        ('plugin', 'Plugin'),   # External plugin/script evaluation
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
    flag = models.CharField(max_length=255)
    flag_type = models.CharField(max_length=10, choices=FLAG_TYPE_CHOICES, default='static')
    points = models.PositiveIntegerField(default=100)
    attachment = models.FileField(  # ✅ New field for challenge files
        upload_to=Challenge_file_upload_path,
        null=True,
        blank=True,
        help_text="Optional file for the challenge (e.g., image, zip, doc)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.difficulty})"

