from django.contrib import admin
from .models import Challenge

@admin.register(Challenge)
class ChallengesAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'points', 'is_active', 'created_at')
    list_filter = ('category', 'difficulty', 'is_active')
    search_fields = ('title', 'description')

