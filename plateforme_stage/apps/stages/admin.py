"""
Admin configuration for the stages app.
"""

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import StageEnCours, VisiteTerrainRapport, MessageInterne


@admin.register(StageEnCours)
class StageEnCoursAdmin(ImportExportModelAdmin):
    """
    Admin interface for Ongoing Internships.
    """
    
    list_display = (
        'etudiant', 'entreprise', 'statut', 'date_debut',
        'date_fin_prevue', 'enseignant_encadrant'
    )
    list_filter = ('statut', 'date_debut')
    search_fields = (
        'etudiant__user__email', 'entreprise__nom_entreprise',
        'sujet_stage'
    )
    readonly_fields = ('date_creation',)
    date_hierarchy = 'date_debut'
    
    fieldsets = (
        ('Internship Details', {
            'fields': ('etudiant', 'entreprise', 'enseignant_encadrant')
        }),
        ('Timeline', {
            'fields': ('date_debut', 'date_fin_prevue', 'date_fin_reelle')
        }),
        ('Project Information', {
            'fields': ('sujet_stage', 'objectifs')
        }),
        ('Documents & Evaluation', {
            'fields': ('convention_stage', 'rapport_final', 'note_finale', 'mention')
        }),
        ('Defense', {
            'fields': ('soutenance_date', 'soutenance_lieu')
        }),
        ('Status', {
            'fields': ('statut',)
        }),
        ('Timestamps', {
            'fields': ('date_creation',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['marquer_comme_termine', 'exporter_conventions']
    
    def marquer_comme_termine(self, request, queryset):
        """Mark selected internships as completed."""
        queryset.update(statut='TERMINE')
        self.message_user(request, f"{queryset.count()} internships marked as completed.")
    marquer_comme_termine.short_description = "Mark as completed"
    
    def exporter_conventions(self, request, queryset):
        """Export internship agreements."""
        # This would generate a ZIP file with all conventions
        self.message_user(request, "Convention export feature to be implemented.")
    exporter_conventions.short_description = "Export conventions"


@admin.register(VisiteTerrainRapport)
class VisiteTerrainRapportAdmin(ImportExportModelAdmin):
    """
    Admin interface for Field Visit Reports.
    """
    
    list_display = (
        'stage', 'semaine_numero', 'auteur', 'avancement',
        'valide_par_enseignant', 'date_soumission'
    )
    list_filter = ('valide_par_enseignant', 'date_soumission')
    search_fields = ('stage__etudiant__user__email', 'auteur__email')
    readonly_fields = ('date_soumission',)
    date_hierarchy = 'date_soumission'
    
    fieldsets = (
        ('Report Information', {
            'fields': ('stage', 'auteur', 'semaine_numero')
        }),
        ('Content', {
            'fields': ('date_rapport', 'avancement', 'taches_realisees', 'difficultes', 'prochaines_etapes')
        }),
        ('Validation', {
            'fields': ('commentaire_enseignant', 'valide_par_enseignant', 'date_validation')
        }),
        ('Timestamps', {
            'fields': ('date_soumission',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['valider_rapports']
    
    def valider_rapports(self, request, queryset):
        """Validate selected reports."""
        from django.utils import timezone
        queryset.update(valide_par_enseignant=True, date_validation=timezone.now())
        self.message_user(request, f"{queryset.count()} reports validated.")
    valider_rapports.short_description = "Validate selected reports"


@admin.register(MessageInterne)
class MessageInterneAdmin(admin.ModelAdmin):
    """
    Admin interface for Internal Messages.
    """
    
    list_display = ('expediteur', 'destinataire', 'sujet', 'lu', 'date_envoi')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('expediteur__email', 'destinataire__email', 'sujet')
    readonly_fields = ('date_envoi',)
    date_hierarchy = 'date_envoi'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('expediteur', 'destinataire', 'stage')
        }),
        ('Content', {
            'fields': ('sujet', 'contenu')
        }),
        ('Status', {
            'fields': ('lu', 'date_envoi')
        }),
    )
