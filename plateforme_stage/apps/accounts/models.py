"""
Accounts app - User profiles and role management.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.models import UserRole


class UserProfile(AbstractUser):
    """
    Custom user model extending AbstractUser with role-based access.
    Each user has a specific role: Student, Company, Teacher, or Admin.
    """
    
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.ETUDIANT,
        verbose_name='Role'
    )
    
    photo_profil = models.ImageField(
        upload_to='profiles/photos/',
        null=True,
        blank=True,
        verbose_name='Profile Photo'
    )
    
    telephone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Phone Number'
    )
    
    adresse = models.TextField(
        null=True,
        blank=True,
        verbose_name='Address'
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Account Created Date'
    )
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    @property
    def is_etudiant(self):
        """Check if user is a student."""
        return self.role == UserRole.ETUDIANT
    
    @property
    def is_entreprise(self):
        """Check if user is a company."""
        return self.role == UserRole.ENTREPRISE
    
    @property
    def is_enseignant(self):
        """Check if user is a teacher."""
        return self.role == UserRole.ENSEIGNANT
    
    @property
    def is_admin_user(self):
        """Check if user is an admin."""
        return self.role == UserRole.ADMIN


class Etudiant(models.Model):
    """
    Student profile extending UserProfile.
    Contains academic information and documents.
    """
    
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='etudiant_profile',
        verbose_name='User'
    )
    
    filiere = models.CharField(
        max_length=100,
        verbose_name='Major/Field of Study'
    )
    
    niveau = models.CharField(
        max_length=2,
        choices=[
            ('L1', 'License Year 1'),
            ('L2', 'License Year 2'),
            ('L3', 'License Year 3'),
            ('M1', 'Master Year 1'),
            ('M2', 'Master Year 2'),
        ],
        verbose_name='Academic Level'
    )
    
    numero_etudiant = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Student ID Number'
    )
    
    cv = models.FileField(
        upload_to='students/cv/',
        null=True,
        blank=True,
        verbose_name='CV (PDF)'
    )
    
    cv_binary = models.BinaryField(
        null=True, 
        blank=True,
        verbose_name='CV Content (Binary)'
    )
    
    cv_filename = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='CV Filename'
    )
    
    lettre_motivation = models.TextField(
        null=True,
        blank=True,
        verbose_name='Cover Letter'
    )
    
    annee_academique = models.CharField(
        max_length=9,
        default='2024-2025',
        verbose_name='Academic Year'
    )
    
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Registration Date'
    )
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['numero_etudiant']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.numero_etudiant}"


class Entreprise(models.Model):
    """
    Company profile extending UserProfile.
    Contains company information and internship offers.
    """
    
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='entreprise_profile',
        verbose_name='User'
    )
    
    nom_entreprise = models.CharField(
        max_length=200,
        verbose_name='Company Name'
    )
    
    secteur_activite = models.CharField(
        max_length=100,
        verbose_name='Industry Sector'
    )
    
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Company Description'
    )
    
    site_web = models.URLField(
        null=True,
        blank=True,
        verbose_name='Website'
    )
    
    logo = models.ImageField(
        upload_to='companies/logos/',
        null=True,
        blank=True,
        verbose_name='Company Logo'
    )
    
    adresse = models.TextField(
        verbose_name='Address'
    )
    
    ville = models.CharField(
        max_length=100,
        verbose_name='City'
    )
    
    nombre_employes = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Number of Employees'
    )
    
    siret = models.CharField(
        max_length=20,
        verbose_name='SIRET/Tax ID'
    )
    
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Registration Date'
    )
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['nom_entreprise']
    
    def __str__(self):
        return self.nom_entreprise


class Enseignant(models.Model):
    """
    Teacher profile extending UserProfile.
    Contains academic department and specialization.
    """
    
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='enseignant_profile',
        verbose_name='User'
    )
    
    departement = models.CharField(
        max_length=100,
        verbose_name='Department'
    )
    
    specialite = models.CharField(
        max_length=100,
        verbose_name='Specialization'
    )
    
    grade = models.CharField(
        max_length=50,
        verbose_name='Academic Rank'
    )
    
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Registration Date'
    )
    
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        ordering = ['user__last_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.departement}"
