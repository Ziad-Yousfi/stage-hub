from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'pfa'

urlpatterns = [
    path('mon-pfa/', views.mon_pfa_view, name='mon_pfa'),
    path('details/<int:pfa_id>/', views.details_pfa_view, name='details_pfa'),
    path('pfa-encadres/', TemplateView.as_view(template_name='core/under_construction.html'), name='pfa_encadres'),
]
