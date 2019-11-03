from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdvertisementsConfig(AppConfig):
    name = "adverge.advertisements"
    verbose_name = _("Advertisements")

    def ready(self):
        # importing signal handlers
        import adverge.advertisements.hooks
