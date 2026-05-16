from django.urls import path
from django.views.generic import TemplateView

app_name = 'notifications'

urlpatterns = [
    path('liste/', TemplateView.as_view(template_name='core/under_construction.html'), name='liste'),

]
