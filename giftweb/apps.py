from django.apps import AppConfig


class GiftwebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'giftweb'

    #def ready(self):
     #   import giftweb.signals 