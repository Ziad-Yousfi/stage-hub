"""
Admin configuration for the offres app.
"""

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Competence, Filiere, OffreStage, Favori


@admin.register(Competence)
class CompetenceAdmin(ImportExportModelAdmin):
    """
    Admin interface for Skills/Competencies.
    """
    
    list_display = ('nom', 'categorie')
    list_filter = ('categorie',)
    search_fields = ('nom', 'categorie')
    ordering = ('nom',)


@admin.register(Filiere)
class FiliereAdmin(ImportExportModelAdmin):
    """
    Admin interface for Academic Majors.
    """
    
    list_display = ('nom', 'description')
    search_fields = ('nom',)
    ordering = ('nom',)


@admin.register(OffreStage)
class OffreStageAdmin(ImportExportModelAdmin):
    """
    Admin interface for Internship Offers.
    """
    
    list_display = (
        'titre', 'entreprise', 'type_stage', 'niveau_requis',
        'localisation', 'statut', 'date_publication'
    )
    list_filter = ('type_stage', 'niveau_requis', 'statut', 'teletravail')
    search_fields = ('titre', 'description', 'entreprise__nom_entreprise')
    readonly_fields = ('date_publication', 'date_modification')
    date_hierarchy = 'date_publication'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('titre', 'description', 'missions')
        }),
        ('Internship Details', {
            'fields': (
                'type_stage', 'duree_semaines', 'date_debut',
                'date_fin_candidature', 'niveau_requis'
            )
        }),
        ('Requirements', {
            'fields': ('competences_requises', 'filieres_ciblees')
        }),
        ('Location & Benefits', {
            'fields': (
                'localisation', 'teletravail',
                'gratification_montant', 'gratification_devise',
                'nombre_postes'
            )
        }),
        ('Company & Status', {
            'fields': ('entreprise', 'statut')
        }),
        ('Timestamps', {
            'fields': ('date_publication', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['publier_offres', 'expirer_offres']
    
    def publier_offres(self, request, queryset):
        """Action to publish selected draft offers."""
        queryset.update(statut='PUBLIEE')
        self.message_user(request, f"{queryset.count()} offers published successfully.")
    publier_offres.short_description = "Publish selected offers"
    
    def expirer_offres(self, request, queryset):
        """Action to expire selected offers."""
        queryset.update(statut='EXPIREE')
        self.message_user(request, f"{queryset.count()} offers marked as expired.")
    expirer_offres.short_description = "Expire selected offers"


@admin.register(Favori)
class FavoriAdmin(admin.ModelAdmin):
    """
    Admin interface for Favorite Offers.
    """
    
    list_display = ('etudiant', 'offre', 'date_ajout')
    list_filter = ('date_ajout',)
    search_fields = ('etudiant__user__email', 'offre__titre')
    readonly_fields = ('date_ajout',)
