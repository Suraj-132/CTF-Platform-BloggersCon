# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.http import HttpResponse 

from rest_framework import permissions

# #  Swagger imports
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# #  Schema view setup
# schema_view = get_schema_view(
#     openapi.Info(
#         title="CTF Platform API",
#         default_version='v1',
#         description="API documentation for your Capture The Flag platform",
#         contact=openapi.Contact(email="your@email.com"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

# def home(request):
#     return HttpResponse("<h2>Welcome to the CTF Platform API</h2>")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/Challenge/', include('Challenge.urls')),
    path('api/teams/', include('teams.urls')),
    path('api/announcements/', include('announcements.urls')),
    # path('', home),

    # #  Swagger & ReDoc documentation routes
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # #  Optional docs app route (if you have one)
    # path('', include('docs.urls')),
]

#  To serve media files (uploads like attachments)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
