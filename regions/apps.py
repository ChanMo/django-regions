from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RegionsConfig(AppConfig):
    name = 'regions'
    verbose_name = _('region')
