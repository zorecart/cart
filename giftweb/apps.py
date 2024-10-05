
#apps.py
from django.apps import AppConfig

class GiftwebConfig(AppConfig):
    name = 'giftweb'

    def ready(self):
        import giftweb.signals  # Import signals here
