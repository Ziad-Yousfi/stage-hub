from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PFA, MessagePFA
from apps.core.ai_services import AIService

@login_required
def mon_pfa_view(request):
    if not request.user.is_etudiant:
        return render(request, 'core/under_construction.html')
    
    if not hasattr(request.user, 'etudiant_profile'):
        messages.info(request, "Veuillez compléter votre profil étudiant avant d'accéder à votre PFA.")
        return redirect('accounts:profile')
        
    # Get existing PFA or create a default one for the student
    etudiant = request.user.etudiant_profile
    pfa = PFA.objects.filter(etudiants=etudiant).first()
    
    if not pfa:
        # Auto-create a default PFA if none exists so the student can use the IA tutor
        pfa = PFA.objects.create(
            titre_pfa=f"Projet PFA de {request.user.get_full_name() or request.user.username}",
            description="Projet de fin d'année en cours de définition. Utilisez le chat avec l'IA pour préciser vos objectifs.",
            domaine="À définir",
            annee_academique="2024-2025",
            statut='EN_COURS'
        )
        pfa.etudiants.add(etudiant)
        messages.success(request, "Votre espace PFA a été initialisé ! Vous pouvez maintenant échanger avec votre tuteur IA.")
    
    return redirect('pfa:details_pfa', pfa_id=pfa.id)

@login_required
def details_pfa_view(request, pfa_id):
    pfa = get_object_or_404(PFA, id=pfa_id)
    
    # Simple security check
    if request.user.is_etudiant and request.user.etudiant_profile not in pfa.etudiants.all():
        return redirect('dashboard:home')
    if request.user.is_enseignant and pfa.encadrant_academique != request.user.enseignant_profile:
        return redirect('dashboard:home')
        
    messages_pfa = pfa.messages.all().order_by('date_envoi')
    
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu:
            # Save student message
            MessagePFA.objects.create(
                pfa=pfa,
                auteur=request.user,
                contenu=contenu
            )
            
            # IA Tutor Logic: Generate response if it's a student messaging
            if request.user.is_etudiant:
                ai = AIService()
                
                # Build context for AI
                pfa_context = {
                    'titre': pfa.titre_pfa,
                    'description': pfa.description,
                    'domaine': pfa.domaine,
                    'etapes': ", ".join([e.titre_etape for e in pfa.etapes.all()])
                }
                
                # Get last 10 messages for history
                history = [
                    {'is_user': m.auteur == request.user, 'text': m.contenu}
                    for m in messages_pfa.order_by('-date_envoi')[:10][::-1]
                ]
                
                ai_response = ai.get_pfa_tutor_response(pfa_context, contenu, history)
                
                # Get or Create AI User (system user)
                from django.contrib.auth import get_user_model
                User = get_user_model()
                ai_user, _ = User.objects.get_or_create(
                    email="ai.tutor@emsi.ma",
                    defaults={
                        'username': 'AI_Tutor', 
                        'first_name': 'Professeur', 
                        'last_name': 'IA (Expert EMSI)'
                    }
                )
                
                MessagePFA.objects.create(
                    pfa=pfa,
                    auteur=ai_user,
                    contenu=ai_response
                )
            
            return redirect('pfa:details_pfa', pfa_id=pfa.id)
            
    context = {
        'pfa': pfa,
        'pfa_messages': messages_pfa,
    }
    return render(request, 'pfa/details.html', context)
