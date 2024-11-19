from django.apps import AppConfig
from django.contrib.auth import get_user_model


class MiAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mi_app'

    def ready(self):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='mmendezm21@curnvirtual.edu.co',
                password='admin'
            )