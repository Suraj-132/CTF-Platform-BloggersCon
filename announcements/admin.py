from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'author']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new announcement
            obj.author = request.user
        super().save_model(request, obj, form, change)
