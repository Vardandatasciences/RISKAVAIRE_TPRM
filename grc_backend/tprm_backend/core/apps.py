"""
Core application configuration for TPRM
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tprm_backend.core'
    verbose_name = 'Core'
