from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.candidatures.models import Candidature
from apps.pfa.models import PFA
from apps.offres.models import OffreStage

@login_required
def home_view(request):
    user = request.user
    context = {}
    
    if user.is_etudiant:
        if hasattr(user, 'etudiant_profile'):
            context['candidatures_count'] = Candidature.objects.filter(etudiant=user.etudiant_profile).count()
            context['pfa'] = PFA.objects.filter(etudiants=user.etudiant_profile).first()
            context['recent_offers'] = OffreStage.objects.filter(statut='PUBLIEE').order_by('-date_publication')[:3]
        else:
            context['profile_missing'] = True
            
    elif user.is_entreprise:
        if hasattr(user, 'entreprise_profile'):
            context['offres_count'] = OffreStage.objects.filter(entreprise=user.entreprise_profile).count()
            context['candidatures_recues'] = Candidature.objects.filter(offre__entreprise=user.entreprise_profile).count()
            
    elif user.is_enseignant:
        if hasattr(user, 'enseignant_profile'):
            context['pfa_encadres'] = PFA.objects.filter(encadrant_academique=user.enseignant_profile).count()

    return render(request, 'dashboard/home.html', context)
