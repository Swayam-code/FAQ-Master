from django.apps import AppConfig


class FaqConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'faq'
    verbose_name = 'FAQ Management'

    def ready(self):
        """Initialize app configurations."""
        from django.conf import settings
        
        # Ensure required settings are available
        if not hasattr(settings, 'CKEDITOR_UPLOAD_PATH'):
            settings.CKEDITOR_UPLOAD_PATH = 'uploads/'
