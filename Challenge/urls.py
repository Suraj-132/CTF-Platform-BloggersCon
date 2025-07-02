from django.urls import path
from .views import ChallengeListView, ChallengeDetailView, SubmitFlagView

urlpatterns = [
    path('', ChallengeListView.as_view(), name='Challenge-list'),
    path('<uuid:id>/', ChallengeDetailView.as_view(), name='Challenge-detail'),
    path('<uuid:challenge_id>/submit-flag/', SubmitFlagView.as_view(), name='submit-flag'),
]
