from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import OffreStage
from apps.core.ai_services import AIService
from apps.core.external_apis import ExternalOffersService

from django.http import JsonResponse

def liste_offres_view(request):
    # Fetch local published offers ONLY (Super Fast)
    offres = OffreStage.objects.filter(statut='PUBLIEE').select_related('entreprise')
    
    domaine = request.GET.get('domaine')
    if domaine:
        offres = offres.filter(filieres_ciblees__nom__icontains=domaine)
        
    context = {
        'offres': offres,
        # We don't fetch external here anymore to save time
    }
    return render(request, 'offres/liste_offres.html', context)

def api_external_offers_view(request):
    """
    Async endpoint to fetch external jobs without blocking the main page.
    """
    domaine = request.GET.get('domaine')
    
    # Fetch RapidAPI
    raw_rapid = ExternalOffersService.get_rapidapi_internships()
    external_offers = [j for j in raw_rapid if isinstance(j, dict)][:15]
    
    # Fetch Ninja
    raw_ninja = ExternalOffersService.get_openwebninja_internships(query=domaine if domaine else "internship")
    ninja_offers = [j for j in raw_ninja if isinstance(j, dict)][:15]
    
    return JsonResponse({
        'rapid': external_offers,
        'ninja': ninja_offers
    })

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
        
    # 2. Collect ALL offers (Local + External)
    local_offres = OffreStage.objects.filter(statut='PUBLIEE')
    rapid_offres = ExternalOffersService.get_rapidapi_internships()
    ninja_offres = ExternalOffersService.get_openwebninja_internships(query="internship")
    
    all_offers_for_ai = []
    
    # Add local
    for o in local_offres:
        all_offers_for_ai.append({
            'id': f"LOCAL_{o.id}",
            'titre': o.titre,
            'entreprise': o.entreprise.nom_entreprise,
            'missions': o.description[:500]
        })
        
    # Add Rapid (limited to top 15)
    for i, o in enumerate(rapid_offres[:15]):
        all_offers_for_ai.append({
            'id': f"EXTERNAL_RAPID_{i}",
            'titre': o.get('title'),
            'entreprise': o.get('company'),
            'missions': o.get('description', '')[:500]
        })

    # Add Ninja (limited to top 15)
    for i, o in enumerate(ninja_offres[:15]):
        all_offers_for_ai.append({
            'id': f"EXTERNAL_NINJA_{i}",
            'titre': o.get('job_title') or o.get('title'),
            'entreprise': o.get('employer_name') or o.get('company'),
            'missions': o.get('job_description', '')[:500]
        })
    
    if not all_offers_for_ai:
        messages.info(request, "Aucune offre (locale ou mondiale) n'est disponible pour le moment.")
        return redirect('offres:liste_offres')
        
    # 3. Call AI for matching
    ai_result_raw = ai.match_cv_to_offers(cv_text, all_offers_for_ai)
    
    try:
        ai_result = json.loads(ai_result_raw)
        best_ids = ai_result.get('best_matches', [])
        explanation = ai_result.get('explanation', "Voici les meilleures opportunités sélectionnées pour votre profil.")
        
        # 4. Filter and Reconstruct the matched objects
        matched_local = []
        matched_external = []
        
        for bid in best_ids:
            bid_str = str(bid).upper()
            if "LOCAL_" in bid_str:
                pk = bid_str.replace("LOCAL_", "")
                obj = local_offres.filter(id=pk).first()
                if obj: matched_local.append(obj)
            elif "EXTERNAL_RAPID_" in bid_str:
                try:
                    idx = int(bid_str.replace("EXTERNAL_RAPID_", ""))
                    if idx < len(rapid_offres):
                        job = rapid_offres[idx]
                        matched_external.append({
                            'title': job.get('title'),
                            'company': job.get('company'),
                            'location': job.get('location'),
                            'url': job.get('url'),
                            'description': job.get('description'),
                            'source': 'RapidAPI'
                        })
                except ValueError: pass
            elif "EXTERNAL_NINJA_" in bid_str:
                try:
                    idx = int(bid_str.replace("EXTERNAL_NINJA_", ""))
                    if idx < len(ninja_offres):
                        job = ninja_offres[idx]
                        matched_external.append({
                            'title': job.get('job_title') or job.get('title'),
                            'company': job.get('employer_name') or job.get('company'),
                            'location': f"{job.get('job_city', '')} {job.get('job_country', '')}".strip() or 'International',
                            'url': job.get('job_apply_link') or job.get('url'),
                            'description': job.get('job_description') or '',
                            'source': 'Ninja'
                        })
                except ValueError: pass
        
        # If AI failed to return prefixed IDs but returned raw numbers (fallback)
        if not matched_local and not matched_external and best_ids:
            # Try to see if it returned local IDs as plain numbers
            matched_local = list(local_offres.filter(id__in=best_ids))

        context = {
            'offres': matched_local,
            'matched_external': matched_external,
            'explanation': explanation,
            'is_ia_matching': True
        }
        return render(request, 'offres/liste_offres.html', context)
        
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        print(f"IA Error: {e}")
        messages.error(request, "L'analyse a pris trop de temps. Veuillez réessayer.")
        return redirect('offres:liste_offres')
