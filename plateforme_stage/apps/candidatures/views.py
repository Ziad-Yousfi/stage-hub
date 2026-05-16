from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Candidature

@login_required
def mes_candidatures_view(request):
    if not request.user.is_etudiant:
        return render(request, 'core/under_construction.html')
    
    if not hasattr(request.user, 'etudiant_profile'):
        messages.info(request, "Veuillez compléter votre profil étudiant avant d'accéder à vos candidatures.")
        return redirect('accounts:profile')
        
    candidatures = Candidature.objects.filter(
        etudiant=request.user.etudiant_profile
    ).select_related('offre', 'offre__entreprise').order_by('-date_candidature')
    
    context = {
        'candidatures': candidatures,
    }
    return render(request, 'candidatures/mes_candidatures.html', context)
