from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'candidatures'

urlpatterns = [
    path('mes-candidatures/', views.mes_candidatures_view, name='mes_candidatures'),
    path('candidatures-recues/', TemplateView.as_view(template_name='core/under_construction.html'), name='candidatures_recues'),
]
