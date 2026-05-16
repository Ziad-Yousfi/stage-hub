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
    from django.conf import settings
    db = getattr(settings, 'FIREBASE_DB', None)
    
    # 1. Security Check
    if request.user.is_etudiant:
        if request.user.etudiant_profile not in pfa.etudiants.all():
            return redirect('dashboard:home')
    elif request.user.is_enseignant:
        if pfa.encadrant_academique != request.user.enseignant_profile:
            return redirect('dashboard:home')
        
    # 2. Get Messages from Firestore
    pfa_messages = []
    if db:
        docs = db.collection('pfa_messages').where('pfa_id', '==', pfa.id).order_by('date_envoi').stream()
        for doc in docs:
            pfa_messages.append(doc.to_dict())

    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        if contenu and db:
            import datetime
            # Save student message to Firestore
            new_msg = {
                'pfa_id': pfa.id,
                'auteur_email': request.user.email,
                'auteur_name': request.user.get_full_name() or request.user.username,
                'is_ai': False,
                'contenu': contenu,
                'date_envoi': datetime.datetime.now()
            }
            db.collection('pfa_messages').add(new_msg)
            
            # IA Tutor Logic: Only respond to student
            if request.user.is_etudiant:
                ai = AIService()
                pfa_context = {
                    'titre': pfa.titre_pfa,
                    'description': pfa.description,
                    'domaine': pfa.domaine,
                    'etapes': ", ".join([e.titre_etape for e in pfa.etapes.all()])
                }
                # Simplify history for AI
                history = [{'is_user': not m.get('is_ai', False), 'text': m.get('contenu', '')} for m in pfa_messages[-5:]]
                ai_response = ai.get_pfa_tutor_response(pfa_context, contenu, history)
                
                # Save AI response to Firestore
                ai_msg = {
                    'pfa_id': pfa.id,
                    'auteur_email': 'ai.tutor@emsi.ma',
                    'auteur_name': 'Professeur IA (Expert EMSI)',
                    'is_ai': True,
                    'contenu': ai_response,
                    'date_envoi': datetime.datetime.now()
                }
                db.collection('pfa_messages').add(ai_msg)
            
            return redirect('pfa:details_pfa', pfa_id=pfa.id)
            
    context = {
        'pfa': pfa,
        'pfa_messages': pfa_messages,
    }
    return render(request, 'pfa/details.html', context)
