from django.urls import path
from .views import TeamLeaderboardView

urlpatterns = [
    path('leaderboard/', TeamLeaderboardView.as_view(), name='team-leaderboard'),
]