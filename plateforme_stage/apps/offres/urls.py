from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'offres'

urlpatterns = [
    path('liste/', views.liste_offres_view, name='liste_offres'),
    path('matching-ia/', views.matching_ia_view, name='matching_ia'),
    path('api/external-offers/', views.api_external_offers_view, name='api_external_offers'),
    path('mes-offres/', TemplateView.as_view(template_name='core/under_construction.html'), name='mes_offres'),
]
