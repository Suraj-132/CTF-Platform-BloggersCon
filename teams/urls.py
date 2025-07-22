from django.urls import path
from .views import (
    TeamListCreateView, 
    TeamDetailView, 
    TeamJoinView, 
    TeamLeaveView, 
    TeamLeaderboardView
)

urlpatterns = [
    path('', TeamListCreateView.as_view(), name='team-list-create'),
    path('<uuid:id>/', TeamDetailView.as_view(), name='team-detail'),
    path('join/', TeamJoinView.as_view(), name='team-join'),
    path('<uuid:team_id>/leave/', TeamLeaveView.as_view(), name='team-leave'),
    path('leaderboard/', TeamLeaderboardView.as_view(), name='team-leaderboard'),
]
