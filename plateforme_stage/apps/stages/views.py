from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StageEnCours

@login_required
def mon_stage_view(request):
    if not request.user.is_etudiant:
        return render(request, 'core/under_construction.html')
    
    if not hasattr(request.user, 'etudiant_profile'):
        messages.info(request, "Veuillez compléter votre profil étudiant avant d'accéder à votre stage.")
        return redirect('accounts:profile')
        
    stage = StageEnCours.objects.filter(etudiant=request.user.etudiant_profile).first()
    
    if not stage:
        return render(request, 'core/under_construction.html', {
            'title': 'Mon Stage',
            'message': "Vous n'avez pas encore de stage actif enregistré. Une fois votre candidature acceptée, votre stage apparaîtra ici."
        })
    
    context = {
        'stage': stage,
        'rapports': stage.rapports.all(),
    }
    return render(request, 'stages/mon_stage.html', context)

@login_required
def stages_encadres_view(request):
    if not request.user.is_enseignant:
        return render(request, 'core/under_construction.html')
        
    stages = StageEnCours.objects.filter(enseignant_encadrant=request.user.enseignant_profile)
    
    return render(request, 'stages/stages_encadres.html', {'stages': stages})
