from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Challenge
from .serializers import ChallengeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response  # To send JSON
from rest_framework import status, permissions  # HTTP codes and access control
from django.shortcuts import get_object_or_404  # To safely get a Challenge
from .models import Challenge  # Your model
from .serializers import FlagSubmissionSerializer  # Serializer that validates flag



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

class SubmitFlagView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, challenge_id):
        challenge = get_object_or_404(Challenge, id=challenge_id)

        # Pass challenge instance into serializer context
        serializer = FlagSubmissionSerializer(data=request.data, context={'challenge': challenge})

        if serializer.is_valid():
            return Response({"message": "Correct flag!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
