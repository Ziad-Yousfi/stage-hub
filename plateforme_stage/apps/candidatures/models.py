"""
Candidatures app - Internship applications and free internship requests.
"""

from django.db import models
from django.conf import settings
from apps.core.models import CandidatureStatus, StageType


class Candidature(models.Model):
    """
    Model representing a student's application to an internship offer.
    Tracks the status and communication between student and company.
    """
    
    etudiant = models.ForeignKey(
        'accounts.Etudiant',
        on_delete=models.CASCADE,
        related_name='candidatures',
        verbose_name='Student'
    )
    
    offre = models.ForeignKey(
        'offres.OffreStage',
        on_delete=models.CASCADE,
        related_name='candidatures',
        verbose_name='Offer'
    )
    
    lettre_motivation = models.TextField(
        null=True,
        blank=True,
        verbose_name='Cover Letter'
    )
    
    cv_version = models.FileField(
        upload_to='candidatures/cv/',
        null=True,
        blank=True,
        verbose_name='CV Version (snapshot)'
    )
    
    statut = models.CharField(
        max_length=20,
        choices=CandidatureStatus.choices,
        default=CandidatureStatus.EN_ATTENTE,
        verbose_name='Status'
    )
    
    date_candidature = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Application Date'
    )
    
    date_derniere_maj = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Updated Date'
    )
    
    message_entreprise = models.TextField(
        null=True,
        blank=True,
        verbose_name='Company Message/Feedback'
    )
    
    note_interne_enseignant = models.TextField(
        null=True,
        blank=True,
        verbose_name='Internal Teacher Note'
    )
    
    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ['-date_candidature']
        unique_together = ['etudiant', 'offre']
        indexes = [
            models.Index(fields=['statut', 'date_candidature']),
            models.Index(fields=['etudiant', 'statut']),
        ]
    
    def __str__(self):
        return f"{self.etudiant.user.get_full_name()} - {self.offre.titre}"
    
    def marquer_comme_vue(self):
        """Mark the application as viewed by the company."""
        if self.statut == CandidatureStatus.EN_ATTENTE:
            self.statut = CandidatureStatus.VUE
            self.save()


class DemandeStageLibre(models.Model):
    """
    Model representing a student's request for a free internship
    (not linked to a published offer).
    """
    
    etudiant = models.ForeignKey(
        'accounts.Etudiant',
        on_delete=models.CASCADE,
        related_name='demandes_libres',
        verbose_name='Student'
    )
    
    domaine_recherche = models.CharField(
        max_length=200,
        verbose_name='Desired Field'
    )
    
    periode_souhaitee = models.CharField(
        max_length=100,
        verbose_name='Desired Period'
    )
    
    type_stage = models.CharField(
        max_length=20,
        choices=StageType.choices,
        verbose_name='Internship Type'
    )
    
    lettre = models.TextField(
        verbose_name='Cover Letter'
    )
    
    cv = models.FileField(
        upload_to='demandes_libres/cv/',
        verbose_name='CV'
    )
    
    statut = models.CharField(
        max_length=20,
        choices=[
            ('EN_ATTENTE', 'Pending'),
            ('VALIDEE', 'Validated'),
            ('ARCHIVEE', 'Archived'),
        ],
        default='EN_ATTENTE',
        verbose_name='Status'
    )
    
    enseignant_referent = models.ForeignKey(
        'accounts.Enseignant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demandes_suivies',
        verbose_name='Supervising Teacher'
    )
    
    date_soumission = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Submission Date'
    )
    
    date_validation = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Validation Date'
    )
    
    class Meta:
        verbose_name = 'Free Internship Request'
        verbose_name_plural = 'Free Internship Requests'
        ordering = ['-date_soumission']
    
    def __str__(self):
        return f"{self.etudiant.user.get_full_name()} - {self.domaine_recherche}"
    
    def valider(self, enseignant=None):
        """Validate the free internship request."""
        from django.utils import timezone
        self.statut = 'VALIDEE'
        self.date_validation = timezone.now()
        if enseignant:
            self.enseignant_referent = enseignant
        self.save()
