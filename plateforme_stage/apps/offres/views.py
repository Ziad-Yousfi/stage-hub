from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import OffreStage
from apps.core.ai_services import AIService
from apps.core.external_apis import ExternalOffersService

def liste_offres_view(request):
    # Fetch local published offers
    offres = OffreStage.objects.filter(statut='PUBLIEE').select_related('entreprise')
    
    # Optional filtering for local offers
    domaine = request.GET.get('domaine')
    if domaine:
        offres = offres.filter(filieres_ciblees__nom__icontains=domaine)
        
    # Fetch RapidAPI offers (External)
    raw_rapid = ExternalOffersService.get_rapidapi_internships()
    external_offers = [j for j in raw_rapid if isinstance(j, dict)][:20]
    
    # Fetch Open Web Ninja offers (External)
    raw_ninja = ExternalOffersService.get_openwebninja_internships(query=domaine if domaine else "internship")
    ninja_offers = [j for j in raw_ninja if isinstance(j, dict)][:20]
    
    context = {
        'offres': offres,
        'external_offers': external_offers,
        'ninja_offers': ninja_offers,
    }
    return render(request, 'offres/liste_offres.html', context)

@login_required
def matching_ia_view(request):
    if not request.user.is_etudiant:
        return redirect('dashboard:home')
        
    etudiant = request.user.etudiant_profile
    if not etudiant.cv:
        messages.warning(request, "Veuillez d'abord uploader votre CV dans votre profil pour utiliser le matching IA.")
        return redirect('accounts:profile')
        
    ai = AIService()
    
    # 1. Extract text from CV
    cv_text = ai.extract_text_from_pdf(etudiant.cv.path)
    if not cv_text:
        messages.error(request, "Impossible de lire votre CV. Assurez-vous qu'il s'agit d'un PDF valide.")
        return redirect('offres:liste_offres')
        
    # 2. Get all published offers
    offres = OffreStage.objects.filter(statut='PUBLIEE')
    offers_data = [
        {
            'id': o.id,
            'titre': o.titre,
            'entreprise': o.entreprise.nom_entreprise,
            'missions': o.missions[:500] # Limit context size
        }
        for o in offres
    ]
    
    if not offers_data:
        messages.info(request, "Aucune offre n'est disponible pour le moment.")
        return redirect('offres:liste_offres')
        
    # 3. Call AI for matching
    ai_result_raw = ai.match_cv_to_offers(cv_text, offers_data)
    
    try:
        ai_result = json.loads(ai_result_raw)
        best_ids = ai_result.get('best_matches', [])
        explanation = ai_result.get('explanation', "L'IA a sélectionné ces offres en fonction de vos compétences.")
        
        # 4. Fetch the actual offer objects
        matched_offres = OffreStage.objects.filter(id__in=best_ids).select_related('entreprise')
        
        context = {
            'offres': matched_offres,
            'explanation': explanation,
            'is_ia_matching': True
        }
        return render(request, 'offres/liste_offres.html', context)
        
    except (json.JSONDecodeError, TypeError) as e:
        print(f"JSON Error: {e} | Raw: {ai_result_raw}")
        messages.error(request, "L'IA a rencontré une erreur lors de l'analyse. Veuillez réessayer.")
        return redirect('offres:liste_offres')
