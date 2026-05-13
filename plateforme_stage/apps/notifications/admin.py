"""
Admin configuration for the notifications app.
"""

from django.contrib import admin
from .models import Notification, EmailTemplate, LogEmail


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for In-App Notifications.
    """
    
    list_display = ('destinataire', 'titre', 'type_notification', 'is_read', 'date_creation')
    list_filter = ('type_notification', 'is_read', 'date_creation')
    search_fields = ('destinataire__email', 'titre', 'message')
    readonly_fields = ('date_creation',)
    date_hierarchy = 'date_creation'
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('destinataire', 'titre', 'message', 'type_notification')
        }),
        ('Status', {
            'fields': ('is_read', 'lien_url', 'date_creation')
        }),
    )
    
    actions = ['marquer_comme_lues']
    
    def marquer_comme_lues(self, request, queryset):
        """Mark selected notifications as read."""
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} notifications marked as read.")
    marquer_comme_lues.short_description = "Mark as read"


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for Email Templates.
    """
    
    list_display = ('nom', 'sujet', 'est_actif', 'date_modification')
    list_filter = ('est_actif',)
    search_fields = ('nom', 'sujet')
    readonly_fields = ('date_modification',)
    
    fieldsets = (
        ('Template Information', {
            'fields': ('nom', 'sujet', 'est_actif')
        }),
        ('Content', {
            'fields': ('contenu_html', 'contenu_texte'),
            'description': 'Use {{ variable }} syntax for dynamic content.'
        }),
        ('Timestamps', {
            'fields': ('date_modification',),
            'classes': ('collapse',)
        }),
    )


@admin.register(LogEmail)
class LogEmailAdmin(admin.ModelAdmin):
    """
    Admin interface for Email Logs.
    """
    
    list_display = ('destinataire', 'sujet', 'statut', 'template', 'date_envoi')
    list_filter = ('statut', 'date_envoi')
    search_fields = ('destinataire', 'sujet')
    readonly_fields = ('date_envoi',)
    date_hierarchy = 'date_envoi'
    
    fieldsets = (
        ('Email Details', {
            'fields': ('destinataire', 'sujet', 'template')
        }),
        ('Status', {
            'fields': ('statut', 'erreur_message', 'date_envoi')
        }),
    )
