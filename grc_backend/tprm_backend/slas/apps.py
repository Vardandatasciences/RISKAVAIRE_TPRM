"""
SLAs application configuration for TPRM
"""
from django.apps import AppConfig


class SlasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tprm_backend.slas'
    verbose_name = 'SLAs'
