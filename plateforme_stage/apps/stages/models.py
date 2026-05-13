"""
Stages app - Management of ongoing internships and field reports.
"""

from django.db import models
from django.conf import settings
from apps.core.models import StageStatus


class StageEnCours(models.Model):
    """
    Model representing an ongoing internship.
    Tracks the internship progress, documents, and evaluation.
    """
    
    etudiant = models.ForeignKey(
        'accounts.Etudiant',
        on_delete=models.CASCADE,
        related_name='stages',
        verbose_name='Student'
    )
    
    entreprise = models.ForeignKey(
        'accounts.Entreprise',
        on_delete=models.CASCADE,
        related_name='stages_accueillis',
        verbose_name='Company'
    )
    
    enseignant_encadrant = models.ForeignKey(
        'accounts.Enseignant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stages_encadres',
        verbose_name='Supervising Teacher'
    )
    
    date_debut = models.DateField(
        verbose_name='Start Date'
    )
    
    date_fin_prevue = models.DateField(
        verbose_name='Expected End Date'
    )
    
    date_fin_reelle = models.DateField(
        null=True,
        blank=True,
        verbose_name='Actual End Date'
    )
    
    sujet_stage = models.CharField(
        max_length=300,
        verbose_name='Internship Topic'
    )
    
    objectifs = models.TextField(
        verbose_name='Objectives'
    )
    
    convention_stage = models.FileField(
        upload_to='stages/conventions/',
        null=True,
        blank=True,
        verbose_name='Internship Agreement (PDF)'
    )
    
    statut = models.CharField(
        max_length=20,
        choices=StageStatus.choices,
        default=StageStatus.PLANIFIE,
        verbose_name='Status'
    )
    
    rapport_final = models.FileField(
        upload_to='stages/rapports/',
        null=True,
        blank=True,
        verbose_name='Final Report (PDF)'
    )
    
    soutenance_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Defense Date'
    )
    
    soutenance_lieu = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Defense Location'
    )
    
    note_finale = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Final Grade'
    )
    
    mention = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Honors'
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date'
    )
    
    class Meta:
        verbose_name = 'Ongoing Internship'
        verbose_name_plural = 'Ongoing Internships'
        ordering = ['-date_debut']
        indexes = [
            models.Index(fields=['statut', 'date_debut']),
            models.Index(fields=['etudiant', 'statut']),
        ]
    
    def __str__(self):
        return f"{self.etudiant.user.get_full_name()} - {self.entreprise.nom_entreprise}"
    
    @property
    def duree_jours(self):
        """Calculate the duration in days."""
        if self.date_fin_reelle:
            delta = self.date_fin_reelle - self.date_debut
            return delta.days
        elif self.date_fin_prevue:
            delta = self.date_fin_prevue - self.date_debut
            return delta.days
        return 0
    
    @property
    def is_completed(self):
        """Check if the internship is completed."""
        return self.statut == StageStatus.TERMINE


class VisiteTerrainRapport(models.Model):
    """
    Model representing a weekly field report submitted by the student.
    Teachers can review and validate each report.
    """
    
    stage = models.ForeignKey(
        StageEnCours,
        on_delete=models.CASCADE,
        related_name='rapports',
        verbose_name='Internship'
    )
    
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rapports_rediges',
        verbose_name='Author'
    )
    
    date_rapport = models.DateField(
        verbose_name='Report Date'
    )
    
    semaine_numero = models.IntegerField(
        verbose_name='Week Number'
    )
    
    avancement = models.IntegerField(
        default=0,
        verbose_name='Progress (%)'
    )
    
    taches_realisees = models.TextField(
        verbose_name='Tasks Completed'
    )
    
    difficultes = models.TextField(
        null=True,
        blank=True,
        verbose_name='Difficulties Encountered'
    )
    
    prochaines_etapes = models.TextField(
        verbose_name='Next Steps'
    )
    
    commentaire_enseignant = models.TextField(
        null=True,
        blank=True,
        verbose_name='Teacher Comment'
    )
    
    valide_par_enseignant = models.BooleanField(
        default=False,
        verbose_name='Validated by Teacher'
    )
    
    date_validation = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Validation Date'
    )
    
    date_soumission = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Submission Date'
    )
    
    class Meta:
        verbose_name = 'Field Visit Report'
        verbose_name_plural = 'Field Visit Reports'
        ordering = ['semaine_numero']
        unique_together = ['stage', 'semaine_numero']
    
    def __str__(self):
        return f"Week {self.semaine_numero} - {self.stage.etudiant.user.get_full_name()}"
    
    def valider(self, commentaire=None):
        """Validate the report as a teacher."""
        from django.utils import timezone
        self.valide_par_enseignant = True
        self.date_validation = timezone.now()
        if commentaire:
            self.commentaire_enseignant = commentaire
        self.save()


class MessageInterne(models.Model):
    """
    Model for internal messaging between students, teachers, and companies.
    """
    
    expediteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_envoyes',
        verbose_name='Sender'
    )
    
    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_recus',
        verbose_name='Recipient'
    )
    
    stage = models.ForeignKey(
        StageEnCours,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True,
        verbose_name='Related Internship'
    )
    
    sujet = models.CharField(
        max_length=200,
        verbose_name='Subject'
    )
    
    contenu = models.TextField(
        verbose_name='Content'
    )
    
    lu = models.BooleanField(
        default=False,
        verbose_name='Read'
    )
    
    date_envoi = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Sent Date'
    )
    
    class Meta:
        verbose_name = 'Internal Message'
        verbose_name_plural = 'Internal Messages'
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"{self.expediteur.email} → {self.destinataire.email}: {self.sujet}"
    
    def marquer_comme_lu(self):
        """Mark the message as read."""
        self.lu = True
        self.save()
