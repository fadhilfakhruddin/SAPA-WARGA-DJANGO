from django.apps import AppConfig


class AvaroappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'avaroapp'

    def ready(self):
        """Impor sinyal saat aplikasi siap."""
        import avaroapp.signals