"""
Admin configuration for the candidatures app.
"""

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Candidature, DemandeStageLibre


@admin.register(Candidature)
class CandidatureAdmin(ImportExportModelAdmin):
    """
    Admin interface for Internship Applications.
    """
    
    list_display = (
        'etudiant', 'offre', 'statut', 'date_candidature',
        'get_entreprise_name'
    )
    list_filter = ('statut', 'date_candidature')
    search_fields = (
        'etudiant__user__email', 'offre__titre',
        'etudiant__user__first_name', 'etudiant__user__last_name'
    )
    readonly_fields = ('date_candidature', 'date_derniere_maj')
    date_hierarchy = 'date_candidature'
    
    fieldsets = (
        ('Application Details', {
            'fields': ('etudiant', 'offre')
        }),
        ('Documents', {
            'fields': ('lettre_motivation', 'cv_version')
        }),
        ('Status & Communication', {
            'fields': ('statut', 'message_entreprise', 'note_interne_enseignant')
        }),
        ('Timestamps', {
            'fields': ('date_candidature', 'date_derniere_maj'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marquer_comme_vue', 'marquer_comme_retenue', 'marquer_comme_acceptee']
    
    def get_entreprise_name(self, obj):
        """Get the company name from the offer."""
        return obj.offre.entreprise.nom_entreprise
    get_entreprise_name.short_description = 'Company'
    
    def marquer_comme_vue(self, request, queryset):
        """Mark selected applications as viewed."""
        queryset.update(statut='VUE')
        self.message_user(request, f"{queryset.count()} applications marked as viewed.")
    marquer_comme_vue.short_description = "Mark as viewed"
    
    def marquer_comme_retenue(self, request, queryset):
        """Mark selected applications as shortlisted."""
        queryset.update(statut='RETENUE')
        self.message_user(request, f"{queryset.count()} applications marked as shortlisted.")
    marquer_comme_retenue.short_description = "Mark as shortlisted"
    
    def marquer_comme_acceptee(self, request, queryset):
        """Mark selected applications as accepted."""
        queryset.update(statut='ACCEPTEE')
        self.message_user(request, f"{queryset.count()} applications marked as accepted.")
    marquer_comme_acceptee.short_description = "Mark as accepted"


@admin.register(DemandeStageLibre)
class DemandeStageLibreAdmin(ImportExportModelAdmin):
    """
    Admin interface for Free Internship Requests.
    """
    
    list_display = (
        'etudiant', 'domaine_recherche', 'type_stage',
        'statut', 'date_soumission', 'enseignant_referent'
    )
    list_filter = ('statut', 'type_stage', 'date_soumission')
    search_fields = ('etudiant__user__email', 'domaine_recherche')
    readonly_fields = ('date_soumission', 'date_validation')
    date_hierarchy = 'date_soumission'
    
    fieldsets = (
        ('Student Information', {
            'fields': ('etudiant',)
        }),
        ('Request Details', {
            'fields': ('domaine_recherche', 'periode_souhaitee', 'type_stage')
        }),
        ('Documents', {
            'fields': ('lettre', 'cv')
        }),
        ('Validation', {
            'fields': ('statut', 'enseignant_referent', 'date_validation')
        }),
        ('Timestamps', {
            'fields': ('date_soumission',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['valider_demandes']
    
    def valider_demandes(self, request, queryset):
        """Validate selected free internship requests."""
        queryset.update(statut='VALIDEE')
        self.message_user(request, f"{queryset.count()} requests validated.")
    valider_demandes.short_description = "Validate selected requests"
