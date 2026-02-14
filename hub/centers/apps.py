from django.apps import AppConfig


class CentersConfig(AppConfig):
    name = 'centers'


    def ready(self):
        import centers.signals