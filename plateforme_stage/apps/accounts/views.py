from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm, EtudiantProfileForm

@login_required
def profile_update_view(request):
    user = request.user
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        
        if user.is_etudiant:
            # Create Etudiant profile if it doesn't exist
            if not hasattr(user, 'etudiant_profile'):
                from .models import Etudiant
                Etudiant.objects.create(user=user, numero_etudiant=f"STU{user.id}", filiere="Non définie", niveau="L1")
                
            etudiant_form = EtudiantProfileForm(request.POST, request.FILES, instance=user.etudiant_profile)
            if user_form.is_valid() and etudiant_form.is_valid():
                user_form.save()
                etudiant_form.save()
                messages.success(request, 'Votre profil a été mis à jour avec succès.')
                return redirect('accounts:profile')
        else:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Votre profil a été mis à jour avec succès.')
                return redirect('accounts:profile')
    else:
        user_form = UserProfileForm(instance=user)
        
        if user.is_etudiant:
            if not hasattr(user, 'etudiant_profile'):
                from .models import Etudiant
                Etudiant.objects.create(user=user, numero_etudiant=f"STU{user.id}", filiere="Non définie", niveau="L1")
            etudiant_form = EtudiantProfileForm(instance=user.etudiant_profile)
        else:
            etudiant_form = None

    context = {
        'user_form': user_form,
        'etudiant_form': etudiant_form,
    }
    return render(request, 'accounts/profile_edit.html', context)
