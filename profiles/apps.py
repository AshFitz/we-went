from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    profile config,
    init ready from signals
    so we can use the signals and begin
    saving profiles and creating.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        from . import signals