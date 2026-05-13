"""
URL Configuration for the internship management platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # Django Allauth authentication
    path('accounts/', include('allauth.urls')),
    
    # App URLs
    path('', include('apps.dashboard.urls', namespace='dashboard')),
    path('offres/', include('apps.offres.urls', namespace='offres')),
    path('candidatures/', include('apps.candidatures.urls', namespace='candidatures')),
    path('stages/', include('apps.stages.urls', namespace='stages')),
    path('pfa/', include('apps.pfa.urls', namespace='pfa')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error pages
handler404 = 'apps.core.views.error_404'
handler500 = 'apps.core.views.error_500'
