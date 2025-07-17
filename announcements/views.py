from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Announcement
from .serializers import AnnouncementSerializer, AnnouncementCreateSerializer, AnnouncementUpdateSerializer

class AnnouncementListView(generics.ListAPIView):
    """List all active announcements for users"""
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Announcement.objects.filter(is_active=True)

class AnnouncementDetailView(generics.RetrieveAPIView):
    """Get a specific announcement"""
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Announcement.objects.filter(is_active=True)

# Admin Views (for staff only)
class AnnouncementAdminListView(generics.ListCreateAPIView):
    """List all announcements and create new ones (admin only)"""
    queryset = Announcement.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnnouncementCreateSerializer
        return AnnouncementSerializer

class AnnouncementAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific announcement (admin only)"""
    queryset = Announcement.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AnnouncementUpdateSerializer
        return AnnouncementSerializer
