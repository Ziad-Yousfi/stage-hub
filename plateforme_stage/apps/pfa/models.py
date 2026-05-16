"""
PFA app - End-of-Year Project management.
"""

from django.db import models
from django.conf import settings
from apps.core.models import PFAStatus, Priority, TaskStatus


class PFA(models.Model):
    """
    Model representing an End-of-Year Project (Projet de Fin d'Année).
    Tracks the project from proposal to final defense.
    """
    
    etudiants = models.ManyToManyField(
        'accounts.Etudiant',
        related_name='pfa',
        verbose_name='Students'
    )
    
    encadrant_academique = models.ForeignKey(
        'accounts.Enseignant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pfa_encadres',
        verbose_name='Academic Supervisor'
    )
    
    encadrant_industriel_nom = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Industry Supervisor Name'
    )
    
    encadrant_industriel_entreprise = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Industry Supervisor Company'
    )
    
    titre_pfa = models.CharField(
        max_length=300,
        verbose_name='Project Title'
    )
    
    description = models.TextField(
        verbose_name='Description'
    )
    
    domaine = models.CharField(
        max_length=100,
        verbose_name='Domain'
    )
    
    mots_cles = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        help_text='Comma-separated keywords',
        verbose_name='Keywords'
    )
    
    annee_academique = models.CharField(
        max_length=9,
        default='2024-2025',
        verbose_name='Academic Year'
    )
    
    semestre = models.CharField(
        max_length=20,
        choices=[
            ('S1', 'Semester 1'),
            ('S2', 'Semester 2'),
            ('S3', 'Semester 3'),
            ('S4', 'Semester 4'),
        ],
        default='S2',
        verbose_name='Semester'
    )
    
    statut = models.CharField(
        max_length=20,
        choices=PFAStatus.choices,
        default=PFAStatus.PROPOSE,
        verbose_name='Status'
    )
    
    note_encadrant = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Supervisor Grade'
    )
    
    note_jury = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Jury Grade'
    )
    
    note_finale = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Final Grade'
    )
    
    rapport_pfa = models.FileField(
        upload_to='pfa/rapports/',
        null=True,
        blank=True,
        verbose_name='Project Report (PDF)'
    )
    
    code_source_url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Source Code URL (GitHub)'
    )
    
    date_soutenance = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Defense Date'
    )
    
    lieu_soutenance = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Defense Location'
    )
    
    membres_jury = models.ManyToManyField(
        'accounts.Enseignant',
        blank=True,
        related_name='pfa_jury',
        verbose_name='Jury Members'
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date'
    )
    
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Modified Date'
    )
    
    class Meta:
        verbose_name = 'End-of-Year Project (PFA)'
        verbose_name_plural = 'End-of-Year Projects (PFA)'
        ordering = ['-annee_academique', '-date_creation']
        indexes = [
            models.Index(fields=['statut', 'annee_academique']),
            models.Index(fields=['domaine', 'statut']),
        ]
    
    def __str__(self):
        return self.titre_pfa
    
    @property
    def get_etudiants_names(self):
        """Return a comma-separated list of student names."""
        return ', '.join([
            e.user.get_full_name() 
            for e in self.etudiants.all()
        ])
    
    @property
    def is_completed(self):
        """Check if the PFA is completed."""
        return self.statut in [PFAStatus.SOUTENU, PFAStatus.ARCHIVE]
    
    def calculer_note_finale(self):
        """Calculate the final grade based on supervisor and jury grades."""
        if self.note_encadrant and self.note_jury:
            self.note_finale = (self.note_encadrant * 0.4) + (self.note_jury * 0.6)
            self.save()


class EtapePFA(models.Model):
    """
    Model representing a step/task in a PFA project.
    Used for Kanban/Gantt visualization and progress tracking.
    """
    
    pfa = models.ForeignKey(
        PFA,
        on_delete=models.CASCADE,
        related_name='etapes',
        verbose_name='Project'
    )
    
    titre_etape = models.CharField(
        max_length=200,
        verbose_name='Step Title'
    )
    
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Description'
    )
    
    date_debut_prevue = models.DateField(
        verbose_name='Planned Start Date'
    )
    
    date_fin_prevue = models.DateField(
        verbose_name='Planned End Date'
    )
    
    date_fin_reelle = models.DateField(
        null=True,
        blank=True,
        verbose_name='Actual End Date'
    )
    
    priorite = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MOYENNE,
        verbose_name='Priority'
    )
    
    statut = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.A_FAIRE,
        verbose_name='Status'
    )
    
    responsable = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Person Responsible'
    )
    
    commentaires = models.TextField(
        null=True,
        blank=True,
        verbose_name='Comments'
    )
    
    ordre = models.IntegerField(
        default=0,
        verbose_name='Order'
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date'
    )
    
    class Meta:
        verbose_name = 'Project Step'
        verbose_name_plural = 'Project Steps'
        ordering = ['ordre', 'date_debut_prevue']
        indexes = [
            models.Index(fields=['statut', 'priorite']),
        ]
    
    def __str__(self):
        return f"{self.titre_etape} ({self.pfa.titre_pfa})"
    
    @property
    def duree_prevue_jours(self):
        """Calculate the planned duration in days."""
        delta = self.date_fin_prevue - self.date_debut_prevue
        return delta.days
    
    @property
    def is_retard(self):
        """Check if the step is delayed."""
        from django.utils import timezone
        if self.statut != TaskStatus.TERMINE:
            return timezone.now().date() > self.date_fin_prevue
        return False
    
    def marquer_terminee(self):
        """Mark the step as completed."""
        from django.utils import timezone
        self.statut = TaskStatus.TERMINE
        self.date_fin_reelle = timezone.now().date()
        self.save()


class ReunionSuivi(models.Model):
    """
    Model representing a follow-up meeting for a PFA project.
    """
    
    pfa = models.ForeignKey(
        PFA,
        on_delete=models.CASCADE,
        related_name='reunions',
        verbose_name='Project'
    )
    
    date_reunion = models.DateTimeField(
        verbose_name='Meeting Date'
    )
    
    participants = models.TextField(
        help_text='Comma-separated list of participants',
        verbose_name='Participants'
    )
    
    compte_rendu = models.TextField(
        verbose_name='Meeting Minutes'
    )
    
    prochaine_echeance = models.DateField(
        null=True,
        blank=True,
        verbose_name='Next Deadline'
    )
    
    actions_a_mener = models.TextField(
        null=True,
        blank=True,
        verbose_name='Action Items'
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date'
    )
    
    class Meta:
        verbose_name = 'Follow-up Meeting'
        verbose_name_plural = 'Follow-up Meetings'
        ordering = ['-date_reunion']
    
    def __str__(self):
        return f"Meeting {self.pfa.titre_pfa} - {self.date_reunion.strftime('%Y-%m-%d')}"


class DocumentPFA(models.Model):
    """
    Model for versioned document uploads related to a PFA.
    """
    
    pfa = models.ForeignKey(
        PFA,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Project'
    )
    
    titre = models.CharField(
        max_length=200,
        verbose_name='Document Title'
    )
    
    fichier = models.FileField(
        upload_to='pfa/documents/',
        verbose_name='File'
    )
    
    version = models.CharField(
        max_length=20,
        default='1.0',
        verbose_name='Version'
    )
    
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Description'
    )
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documents_pfa_uploaded',
        verbose_name='Uploaded By'
    )
    
    date_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Upload Date'
    )
    
    class Meta:
        verbose_name = 'PFA Document'
        verbose_name_plural = 'PFA Documents'
        ordering = ['-date_upload']
    
    def __str__(self):
        return f"{self.titre} (v{self.version}) - {self.pfa.titre_pfa}"

class MessagePFA(models.Model):
    """
    Model for discussion messages between a student and their supervisor on a PFA project.
    """
    
    pfa = models.ForeignKey(
        PFA,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Project'
    )
    
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_pfa',
        verbose_name='Author'
    )
    
    contenu = models.TextField(
        verbose_name='Content'
    )
    
    date_envoi = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Sent Date'
    )
    
    class Meta:
        verbose_name = 'PFA Message'
        verbose_name_plural = 'PFA Messages'
        ordering = ['date_envoi']
    
    def __str__(self):
        return f"Message from {self.auteur.email} on {self.pfa.titre_pfa}"
