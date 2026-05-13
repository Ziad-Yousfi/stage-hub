"""
Notifications app - In-app notifications and email alerts.
"""

from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Model representing an in-app notification for users.
    Notifications are created for important events and status changes.
    """
    
    NOTIFICATION_TYPES = [
        ('INSCRIPTION', 'Account Registration'),
        ('CANDIDATURE_STATUT', 'Application Status Change'),
        ('NOUVELLE_CANDIDATURE', 'New Application Received'),
        ('RAPPORT_EN_ATTENTE', 'Report Pending Review'),
        ('RAPPEL_SOUTENANCE', 'Defense Reminder'),
        ('ATTRIBUTION_ENCADRANT', 'Supervisor Assignment'),
        ('MESSAGE_NOUVEAU', 'New Message'),
        ('OFFRE_EXPIREE', 'Offer Expired'),
        ('GENERAL', 'General Notification'),
    ]
    
    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Recipient'
    )
    
    titre = models.CharField(
        max_length=200,
        verbose_name='Title'
    )
    
    message = models.TextField(
        verbose_name='Message'
    )
    
    type_notification = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES,
        default='GENERAL',
        verbose_name='Notification Type'
    )
    
    is_read = models.BooleanField(
        default=False,
        verbose_name='Read'
    )
    
    lien_url = models.URLField(
        null=True,
        blank=True,
        verbose_name='Related URL'
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date'
    )
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['destinataire', 'is_read']),
            models.Index(fields=['type_notification', 'date_creation']),
        ]
    
    def __str__(self):
        return f"{self.destinataire.email} - {self.titre}"
    
    def marquer_comme_lue(self):
        """Mark the notification as read."""
        self.is_read = True
        self.save()


class EmailTemplate(models.Model):
    """
    Model for storing email templates used for transactional emails.
    Allows customization of email content without code changes.
    """
    
    TEMPLATE_TYPES = [
        ('INSCRIPTION_BIENVENUE', 'Welcome Email'),
        ('CANDIDATURE_RECUE', 'Application Received'),
        ('CANDIDATURE_STATUT_CHANGE', 'Application Status Changed'),
        ('RAPPEL_RAPPORT_HEBO', 'Weekly Report Reminder'),
        ('RAPPEL_SOUTENANCE_J7', 'Defense Reminder J-7'),
        ('RAPPEL_SOUTENANCE_J1', 'Defense Reminder J-1'),
        ('ATTRIBUTION_ENCADRANT', 'Supervisor Assignment'),
        ('VALIDATION_COMPTE', 'Account Validation'),
    ]
    
    nom = models.CharField(
        max_length=50,
        choices=TEMPLATE_TYPES,
        unique=True,
        verbose_name='Template Name'
    )
    
    sujet = models.CharField(
        max_length=300,
        verbose_name='Email Subject'
    )
    
    contenu_html = models.TextField(
        help_text='HTML content of the email. Use {{ variable }} for dynamic content.',
        verbose_name='HTML Content'
    )
    
    contenu_texte = models.TextField(
        help_text='Plain text version of the email.',
        verbose_name='Plain Text Content',
        null=True,
        blank=True
    )
    
    est_actif = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Modified Date'
    )
    
    class Meta:
        verbose_name = 'Email Template'
        verbose_name_plural = 'Email Templates'
    
    def __str__(self):
        return self.get_nom_display()


class LogEmail(models.Model):
    """
    Model for logging sent emails for audit purposes.
    """
    
    destinataire = models.EmailField(
        verbose_name='Recipient Email'
    )
    
    sujet = models.CharField(
        max_length=300,
        verbose_name='Subject'
    )
    
    template = models.ForeignKey(
        EmailTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='logs',
        verbose_name='Template Used'
    )
    
    statut = models.CharField(
        max_length=20,
        choices=[
            ('ENVOYE', 'Sent'),
            ('ECHEC', 'Failed'),
            ('EN_ATTENTE', 'Pending'),
        ],
        default='EN_ATTENTE',
        verbose_name='Status'
    )
    
    erreur_message = models.TextField(
        null=True,
        blank=True,
        verbose_name='Error Message'
    )
    
    date_envoi = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Sent Date'
    )
    
    class Meta:
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"{self.destinataire} - {self.sujet}"
