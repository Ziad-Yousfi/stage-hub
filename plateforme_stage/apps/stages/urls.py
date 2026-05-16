from django.urls import path
from .views import mon_stage_view, stages_encadres_view

app_name = 'stages'

urlpatterns = [
    path('mon_stage/', mon_stage_view, name='mon_stage'),
    path('stages_encadres/', stages_encadres_view, name='stages_encadres'),
]
