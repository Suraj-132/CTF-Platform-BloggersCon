from django.urls import path
from .views import (
    AnnouncementListView,
    AnnouncementDetailView,
    AnnouncementAdminListView,
    AnnouncementAdminDetailView
)

urlpatterns = [
    # Public endpoints for users
    path('', AnnouncementListView.as_view(), name='announcement-list'),
    path('<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    
    # Admin endpoints
    path('admin/', AnnouncementAdminListView.as_view(), name='announcement-admin-list'),
    path('admin/<int:pk>/', AnnouncementAdminDetailView.as_view(), name='announcement-admin-detail'),
]
