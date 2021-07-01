from django.apps import AppConfig

class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):

        from . import database_update_service

        #database_update_service.initialize()
        database_update_service.updateDatabase()
