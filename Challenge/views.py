from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Challenge
from .serializers import ChallengeSerializer

# ✅ List all active challenges
class ChallengeListView(generics.ListAPIView):
    queryset = Challenge.objects.filter(is_active=True)
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]

# ✅ Get details of a single challenge
class ChallengeDetailView(generics.RetrieveAPIView):
    queryset = Challenge.objects.filter(is_active=True)
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
