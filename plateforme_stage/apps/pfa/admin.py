"""
Admin configuration for the PFA app.
"""

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import PFA, EtapePFA, ReunionSuivi, DocumentPFA


@admin.register(PFA)
class PFAAdmin(ImportExportModelAdmin):
    """
    Admin interface for End-of-Year Projects.
    """
    
    list_display = (
        'titre_pfa', 'domaine', 'annee_academique', 'semestre',
        'statut', 'note_finale', 'date_soutenance'
    )
    list_filter = ('statut', 'domaine', 'annee_academique', 'semestre')
    search_fields = ('titre_pfa', 'description', 'etudiants__user__email')
    readonly_fields = ('date_creation', 'date_modification')
    date_hierarchy = 'date_soutenance'
    filter_horizontal = ('etudiants', 'membres_jury')
    
    fieldsets = (
        ('Project Information', {
            'fields': ('titre_pfa', 'description', 'domaine', 'mots_cles')
        }),
        ('Students', {
            'fields': ('etudiants',)
        }),
        ('Supervisors', {
            'fields': ('encadrant_academique', 'encadrant_industriel_nom', 'encadrant_industriel_entreprise')
        }),
        ('Academic Details', {
            'fields': ('annee_academique', 'semestre', 'statut')
        }),
        ('Grades', {
            'fields': ('note_encadrant', 'note_jury', 'note_finale')
        }),
        ('Defense & Documents', {
            'fields': ('rapport_pfa', 'code_source_url', 'date_soutenance', 'lieu_soutenance', 'membres_jury')
        }),
        ('Timestamps', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['calculer_notes_finales', 'marquer_comme_soutenu']
    
    def calculer_notes_finales(self, request, queryset):
        """Calculate final grades for selected PFAs."""
        count = 0
        for pfa in queryset:
            if pfa.note_encadrant and pfa.note_jury:
                pfa.calculer_note_finale()
                count += 1
        self.message_user(request, f"{count} final grades calculated.")
    calculer_notes_finales.short_description = "Calculate final grades"
    
    def marquer_comme_soutenu(self, request, queryset):
        """Mark selected PFAs as defended."""
        queryset.update(statut='SOUTENU')
        self.message_user(request, f"{queryset.count()} PFAs marked as defended.")
    marquer_comme_soutenu.short_description = "Mark as defended"


@admin.register(EtapePFA)
class EtapePFAAdmin(ImportExportModelAdmin):
    """
    Admin interface for PFA Project Steps.
    """
    
    list_display = (
        'titre_etape', 'pfa', 'statut', 'priorite',
        'date_debut_prevue', 'date_fin_prevue', 'is_retard'
    )
    list_filter = ('statut', 'priorite', 'is_retard')
    search_fields = ('titre_etape', 'pfa__titre_pfa')
    ordering = ('ordre', 'date_debut_prevue')
    
    fieldsets = (
        ('Step Information', {
            'fields': ('pfa', 'titre_etape', 'description')
        }),
        ('Timeline', {
            'fields': ('date_debut_prevue', 'date_fin_prevue', 'date_fin_reelle')
        }),
        ('Details', {
            'fields': ('priorite', 'statut', 'responsable', 'commentaires', 'ordre')
        }),
    )
    
    actions = ['marquer_comme_terminee']
    
    def marquer_comme_terminee(self, request, queryset):
        """Mark selected steps as completed."""
        from django.utils import timezone
        for etape in queryset:
            etape.marquer_terminee()
        self.message_user(request, f"{queryset.count()} steps marked as completed.")
    marquer_comme_terminee.short_description = "Mark as completed"


@admin.register(ReunionSuivi)
class ReunionSuiviAdmin(admin.ModelAdmin):
    """
    Admin interface for Follow-up Meetings.
    """
    
    list_display = ('pfa', 'date_reunion', 'participants', 'prochaine_echeance')
    list_filter = ('date_reunion',)
    search_fields = ('pfa__titre_pfa', 'compte_rendu')
    date_hierarchy = 'date_reunion'
    
    fieldsets = (
        ('Meeting Information', {
            'fields': ('pfa', 'date_reunion', 'participants')
        }),
        ('Content', {
            'fields': ('compte_rendu', 'prochaine_echeance', 'actions_a_mener')
        }),
    )


@admin.register(DocumentPFA)
class DocumentPFAAdmin(admin.ModelAdmin):
    """
    Admin interface for PFA Documents.
    """
    
    list_display = ('titre', 'pfa', 'version', 'uploaded_by', 'date_upload')
    list_filter = ('date_upload',)
    search_fields = ('titre', 'pfa__titre_pfa')
    readonly_fields = ('date_upload',)
    date_hierarchy = 'date_upload'
    
    fieldsets = (
        ('Document Information', {
            'fields': ('pfa', 'titre', 'fichier', 'version')
        }),
        ('Details', {
            'fields': ('description', 'uploaded_by', 'date_upload')
        }),
    )
