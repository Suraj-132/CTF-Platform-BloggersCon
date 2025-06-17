from django.urls import path
from .views import ChallengeListView, ChallengeDetailView

urlpatterns = [
    path('', ChallengeListView.as_view(), name='Challenge-list'),
    path('<uuid:id>/', ChallengeDetailView.as_view(), name='Challenge-detail'),
]
