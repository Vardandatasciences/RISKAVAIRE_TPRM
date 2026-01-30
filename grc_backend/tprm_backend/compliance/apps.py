"""
Compliance application configuration for TPRM
"""
from django.apps import AppConfig


class ComplianceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tprm_backend.compliance'
    verbose_name = 'Compliance'
