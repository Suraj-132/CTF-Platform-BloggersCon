from django.contrib import admin
from .models import Team, TeamSolve

class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'score']
    readonly_fields = ('score',)  # ✅ Make score read-only in admin form
    filter_horizontal = ('members',)  # Optional: for better UX with many-to-many fields

admin.site.register(Team, TeamAdmin)

from django.contrib import admin
from .models import Team, TeamSolve

class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'score']
    readonly_fields = ('score',)  # ✅ Make score read-only in admin form
    filter_horizontal = ('members',)  # Optional: for better UX with many-to-many fields

@admin.register(TeamSolve)
class TeamSolveAdmin(admin.ModelAdmin):
    list_display = ['team', 'challenge', 'timestamp']
    readonly_fields = ['team', 'challenge', 'timestamp']

    def has_add_permission(self, request):
        return False  # Disallow adding from admin

    def has_change_permission(self, request, obj=None):
        return False  # Disallow changing entries

    def has_delete_permission(self, request, obj=None):
        return False  # Optional: Disallow deleting too

