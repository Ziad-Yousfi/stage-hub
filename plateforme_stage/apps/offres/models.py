"""
Offres app - Internship offers management.
"""

from django.db import models
from django.conf import settings
from apps.core.models import StageType, AcademicLevel, OffreStatus


class Competence(models.Model):
    """
    Model representing skills/competencies required for internships.
    Used for filtering and matching students with offers.
    """
    
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Skill Name'
    )
    
    categorie = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Category'
    )
    
    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Filiere(models.Model):
    """
    Model representing academic majors/fields of study.
    Used to target specific student populations.
    """
    
    nom = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Major Name'
    )
    
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Description'
    )
    
    class Meta:
        verbose_name = 'Major'
        verbose_name_plural = 'Majors'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class OffreStage(models.Model):
    """
    Model representing an internship offer published by a company.
    Contains all details about the internship opportunity.
    """
    
    titre = models.CharField(
        max_length=200,
        verbose_name='Title'
    )
    
    description = models.TextField(
        verbose_name='Description'
    )
    
    missions = models.TextField(
        verbose_name='Missions and Responsibilities'
    )
    
    type_stage = models.CharField(
        max_length=20,
        choices=StageType.choices,
        verbose_name='Internship Type'
    )
    
    duree_semaines = models.IntegerField(
        default=8,
        verbose_name='Duration (weeks)'
    )
    
    date_debut = models.DateField(
        verbose_name='Start Date'
    )
    
    date_fin_candidature = models.DateField(
        verbose_name='Application Deadline'
    )
    
    competences_requises = models.ManyToManyField(
        Competence,
        blank=True,
        related_name='offres',
        verbose_name='Required Skills'
    )
    
    niveau_requis = models.CharField(
        max_length=2,
        choices=AcademicLevel.choices,
        verbose_name='Required Level'
    )
    
    filieres_ciblees = models.ManyToManyField(
        Filiere,
        blank=True,
        related_name='offres',
        verbose_name='Targeted Majors'
    )
    
    localisation = models.CharField(
        max_length=200,
        verbose_name='Location'
    )
    
    teletravail = models.BooleanField(
        default=False,
        verbose_name='Remote Work Available'
    )
    
    gratification_montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Stipend Amount'
    )
    
    gratification_devise = models.CharField(
        max_length=3,
        default='EUR',
        verbose_name='Currency'
    )
    
    nombre_postes = models.IntegerField(
        default=1,
        verbose_name='Number of Positions'
    )
    
    statut = models.CharField(
        max_length=20,
        choices=OffreStatus.choices,
        default=OffreStatus.BROUILLON,
        verbose_name='Status'
    )
    
    entreprise = models.ForeignKey(
        'accounts.Entreprise',
        on_delete=models.CASCADE,
        related_name='offres',
        verbose_name='Company'
    )
    
    date_publication = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publication Date'
    )
    
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Modified Date'
    )
    
    class Meta:
        verbose_name = 'Internship Offer'
        verbose_name_plural = 'Internship Offers'
        ordering = ['-date_publication']
        indexes = [
            models.Index(fields=['statut', 'date_publication']),
            models.Index(fields=['type_stage', 'niveau_requis']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.entreprise.nom_entreprise}"
    
    @property
    def is_expired(self):
        """Check if the application deadline has passed."""
        from django.utils import timezone
        return timezone.now().date() > self.date_fin_candidature
    
    @property
    def candidatures_count(self):
        """Return the number of applications for this offer."""
        return self.candidatures.count()
    
    @property
    def is_accepting_applications(self):
        """Check if the offer is still accepting applications."""
        return (
            self.statut == OffreStatus.PUBLIEE 
            and not self.is_expired
            and self.nombre_postes > 0
        )


class Favori(models.Model):
    """
    Model representing a student's favorite internship offers.
    Allows students to save offers for later review.
    """
    
    etudiant = models.ForeignKey(
        'accounts.Etudiant',
        on_delete=models.CASCADE,
        related_name='favoris',
        verbose_name='Student'
    )
    
    offre = models.ForeignKey(
        OffreStage,
        on_delete=models.CASCADE,
        related_name='favoris',
        verbose_name='Offer'
    )
    
    date_ajout = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Added Date'
    )
    
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='Personal Notes'
    )
    
    class Meta:
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'
        unique_together = ['etudiant', 'offre']
        ordering = ['-date_ajout']
    
    def __str__(self):
        return f"{self.etudiant.user.get_full_name()} - {self.offre.titre}"
