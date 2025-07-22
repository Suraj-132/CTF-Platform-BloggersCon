# teams/views.py
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db.models import Max
from django.shortcuts import get_object_or_404
from .models import Team, TeamSolve
from .serializers import (
    TeamSerializer, 
    TeamCreateSerializer, 
    TeamJoinSerializer, 
    TeamLeaderboardSerializer,
    TeamUpdateSerializer,
    TeamLeaveSerializer
)

class TeamListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamSerializer

    def get_queryset(self):
        return Team.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TeamCreateSerializer
        return TeamSerializer

    def perform_create(self, serializer):
        serializer.save(captain=self.request.user)

class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Team.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TeamUpdateSerializer
        return TeamSerializer

class TeamJoinView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TeamJoinSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        team = serializer.save()
        return Response({"message": f"Joined team {team.name}."})

class TeamLeaveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, team_id):
        team = get_object_or_404(Team, id=team_id)
        
        serializer = TeamLeaveSerializer(data=request.data, context={'request': request, 'team': team})
        serializer.is_valid(raise_exception=True)
        team = serializer.save()
        
        if team is None:
            return Response({"message": "Team deleted as you were the last member."})

        return Response({"message": "Left the team successfully."})

class TeamLeaderboardView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeamLeaderboardSerializer

    def get_queryset(self):
        return Team.objects.annotate(
            last_solve=Max('team_solves__timestamp')
        ).order_by('-score', 'last_solve')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        leaderboard = self.add_ranking(serializer.data)
        return Response(leaderboard)

    def add_ranking(self, data):
        rank = 0
        previous_score = None
        previous_time = None

        for index, item in enumerate(data, start=1):
            score = item['score']
            last_solve = item['last_solve']

            if score != previous_score or last_solve != previous_time:
                rank = index
                previous_score = score
                previous_time = last_solve

            item['rank'] = rank

        return data
