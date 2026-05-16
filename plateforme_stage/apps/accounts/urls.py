from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.profile_update_view, name='profile'),
]
