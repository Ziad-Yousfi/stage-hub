"""
Admin configuration for the accounts app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, Etudiant, Entreprise, Enseignant


@admin.register(UserProfile)
class UserProfileAdmin(BaseUserAdmin):
    """
    Admin interface for UserProfile.
    Extends Django's default UserAdmin with role information.
    """
    
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'date_creation')
    list_filter = ('role', 'is_staff', 'is_active', 'date_creation')
    search_fields = ('email', 'first_name', 'last_name', 'telephone')
    ordering = ('-date_creation',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'photo_profil', 'telephone', 'adresse', 'date_creation')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'photo_profil', 'telephone', 'adresse')
        }),
    )


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    """
    Admin interface for Student profiles.
    """
    
    list_display = ('user', 'numero_etudiant', 'filiere', 'niveau', 'annee_academique')
    list_filter = ('niveau', 'filiere', 'annee_academique')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'numero_etudiant')
    readonly_fields = ('date_inscription',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Academic Information', {
            'fields': ('filiere', 'niveau', 'numero_etudiant', 'annee_academique')
        }),
        ('Documents', {
            'fields': ('cv', 'lettre_motivation')
        }),
        ('Registration', {
            'fields': ('date_inscription',)
        }),
    )


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    """
    Admin interface for Company profiles.
    """
    
    list_display = ('nom_entreprise', 'ville', 'secteur_activite', 'nombre_employes', 'date_inscription')
    list_filter = ('secteur_activite', 'ville')
    search_fields = ('nom_entreprise', 'user__email', 'siret')
    readonly_fields = ('date_inscription',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Company Information', {
            'fields': ('nom_entreprise', 'secteur_activite', 'description', 'site_web')
        }),
        ('Contact Details', {
            'fields': ('logo', 'adresse', 'ville', 'nombre_employes', 'siret')
        }),
        ('Registration', {
            'fields': ('date_inscription',)
        }),
    )


@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    """
    Admin interface for Teacher profiles.
    """
    
    list_display = ('user', 'departement', 'specialite', 'grade', 'date_inscription')
    list_filter = ('departement', 'grade')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'departement')
    readonly_fields = ('date_inscription',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Academic Information', {
            'fields': ('departement', 'specialite', 'grade')
        }),
        ('Registration', {
            'fields': ('date_inscription',)
        }),
    )
