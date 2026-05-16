from django import forms
from .models import UserProfile, Etudiant

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'photo_profil', 'telephone', 'adresse']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_profil': forms.FileInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class EtudiantProfileForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['filiere', 'niveau', 'cv', 'lettre_motivation']
        widgets = {
            'filiere': forms.TextInput(attrs={'class': 'form-control'}),
            'niveau': forms.Select(attrs={'class': 'form-select'}),
            'cv': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'lettre_motivation': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
