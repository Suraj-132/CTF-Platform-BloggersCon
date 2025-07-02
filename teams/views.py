# teams/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Max
from .models import Team, TeamSolve

class TeamLeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teams = Team.objects.all()
        leaderboard_data = []

        for team in teams:
            last_solve = TeamSolve.objects.filter(team=team).aggregate(
                last_solve=Max('timestamp')
            )['last_solve']

            leaderboard_data.append({
                'team': team,
                'score': team.score,
                'last_solve': last_solve,
            })

        leaderboard_data.sort(key=lambda x: (-x['score'], x['last_solve'] or '9999-12-31'))

        leaderboard = []
        rank = 0
        previous_score = None
        previous_time = None

        for index, item in enumerate(leaderboard_data, start=1):
            team = item['team']
            score = item['score']
            last_solve = item['last_solve']

            if score != previous_score or last_solve != previous_time:
                rank = index
                previous_score = score
                previous_time = last_solve

            leaderboard.append({
                'rank': rank,
                'team_name': team.name,
                'score': score,
                'last_solve': last_solve,
                'members': [member.username for member in team.members.all()],
            })

        return Response(leaderboard)
