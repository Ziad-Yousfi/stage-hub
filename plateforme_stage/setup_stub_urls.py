import os

template_code = """from django.urls import path
from django.views.generic import TemplateView

app_name = '{app}'

urlpatterns = [
{paths}
]
"""

apps_paths = {
    'offres': ['liste_offres', 'mes_offres'],
    'candidatures': ['mes_candidatures', 'candidatures_recues'],
    'stages': ['mon_stage', 'stages_encadres'],
    'pfa': ['mon_pfa', 'pfa_encadres'],
    'notifications': ['liste'],
    'accounts': ['profile'],
}

for app, routes in apps_paths.items():
    # Ensure directory exists for accounts/urls.py if not there
    os.makedirs(f'apps/{app}', exist_ok=True)
    
    paths_code = ""
    for route in routes:
        paths_code += f"    path('{route}/', TemplateView.as_view(template_name='core/under_construction.html'), name='{route}'),\n"
        
    with open(f'apps/{app}/urls.py', 'w', encoding='utf-8') as f:
        f.write(template_code.format(app=app, paths=paths_code))

# Update config/urls.py to include accounts namespace
config_urls_path = 'config/urls.py'
with open(config_urls_path, 'r', encoding='utf-8') as f:
    content = f.read()

if "path('accounts/profile/', include('apps.accounts.urls', namespace='accounts'))," not in content:
    new_content = content.replace(
        "path('accounts/', include('allauth.urls')),",
        "path('accounts/', include('allauth.urls')),\n    path('accounts/profile/', include('apps.accounts.urls', namespace='accounts')),"
    )
    with open(config_urls_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Stubs created successfully!")
