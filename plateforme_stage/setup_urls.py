import os

apps = ['dashboard', 'offres', 'candidatures', 'stages', 'pfa', 'notifications']
content = """from django.urls import path
app_name='{}'
urlpatterns=[]
"""

for app in apps:
    with open(f'apps/{app}/urls.py', 'w', encoding='utf-8') as f:
        f.write(content.format(app))
