"""
Core app - Shared models, utilities, and mixins for the internship management platform.
"""

from django.db import models
from django.core.exceptions import PermissionDenied


class UserRole(models.TextChoices):
    """Enumeration of user roles in the platform."""
    ETUDIANT = 'ETUDIANT', 'Student'
    ENTREPRISE = 'ENTREPRISE', 'Company'
    ENSEIGNANT = 'ENSEIGNANT', 'Teacher'
    ADMIN = 'ADMIN', 'Administrator'


class StageType(models.TextChoices):
    """Enumeration of internship types."""
    INITIATION = 'INITIATION', 'Initiation Internship'
    PERFECTIONNEMENT = 'PERFECTIONNEMENT', 'Advanced Internship'
    PFA = 'PFA', 'End-of-Year Project (PFA)'
    PFE = 'PFE', 'End-of-Studies Project (PFE)'


class AcademicLevel(models.TextChoices):
    """Enumeration of academic levels."""
    L1 = 'L1', 'License Year 1'
    L2 = 'L2', 'License Year 2'
    L3 = 'L3', 'License Year 3'
    M1 = 'M1', 'Master Year 1'
    M2 = 'M2', 'Master Year 2'


class CandidatureStatus(models.TextChoices):
    """Enumeration of application statuses."""
    EN_ATTENTE = 'EN_ATTENTE', 'Pending'
    VUE = 'VUE', 'Viewed'
    RETENUE = 'RETENUE', 'Shortlisted'
    REFUSEE = 'REFUSEE', 'Rejected'
    ACCEPTEE = 'ACCEPTEE', 'Accepted'


class OffreStatus(models.TextChoices):
    """Enumeration of job offer statuses."""
    BROUILLON = 'BROUILLON', 'Draft'
    PUBLIEE = 'PUBLIEE', 'Published'
    EXPIREE = 'EXPIREE', 'Expired'
    POURVUE = 'POURVUE', 'Filled'


class StageStatus(models.TextChoices):
    """Enumeration of internship statuses."""
    PLANIFIE = 'PLANIFIE', 'Planned'
    EN_COURS = 'EN_COURS', 'In Progress'
    SUSPENDU = 'SUSPENDU', 'Suspended'
    TERMINE = 'TERMINE', 'Completed'


class PFAStatus(models.TextChoices):
    """Enumeration of PFA statuses."""
    PROPOSE = 'PROPOSE', 'Proposed'
    VALIDE = 'VALIDE', 'Validated'
    EN_COURS = 'EN_COURS', 'In Progress'
    SOUTENU = 'SOUTENU', 'Defended'
    ARCHIVE = 'ARCHIVE', 'Archived'


class Priority(models.TextChoices):
    """Enumeration of priority levels."""
    HAUTE = 'HAUTE', 'High'
    MOYENNE = 'MOYENNE', 'Medium'
    BASSE = 'BASSE', 'Low'


class TaskStatus(models.TextChoices):
    """Enumeration of task statuses for PFA steps."""
    A_FAIRE = 'A_FAIRE', 'To Do'
    EN_COURS = 'EN_COURS', 'In Progress'
    TERMINE = 'TERMINE', 'Completed'
    BLOQUE = 'BLOQUE', 'Blocked'


# =============================================================================
# MIXINS FOR ROLE-BASED ACCESS CONTROL
# =============================================================================

from django.contrib.auth.mixins import UserPassesTestMixin

class RoleRequiredMixin(UserPassesTestMixin):
    """
    Mixin to restrict access based on user role.
    Subclasses must define the required_role attribute.
    """
    required_role = None
    
    def test_func(self):
        if self.required_role is None:
            raise ValueError("required_role must be defined")
        
        user = self.request.user
        if not user.is_authenticated:
            return False
        
        return user.role == self.required_role


class EtudiantRequiredMixin(RoleRequiredMixin):
    """Mixin to restrict access to students only."""
    required_role = UserRole.ETUDIANT


class EntrepriseRequiredMixin(RoleRequiredMixin):
    """Mixin to restrict access to companies only."""
    required_role = UserRole.ENTREPRISE


class EnseignantRequiredMixin(RoleRequiredMixin):
    """Mixin to restrict access to teachers only."""
    required_role = UserRole.ENSEIGNANT


class AdminRequiredMixin(RoleRequiredMixin):
    """Mixin to restrict access to administrators only."""
    required_role = UserRole.ADMIN


class StaffOrAdminRequiredMixin(UserPassesTestMixin):
    """Mixin to restrict access to staff or admin users."""
    
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_staff or user.role == UserRole.ADMIN)
