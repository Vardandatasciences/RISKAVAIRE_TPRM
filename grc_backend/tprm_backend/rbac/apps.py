"""
RBAC application configuration for TPRM
"""
from django.apps import AppConfig


class RbacConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tprm_backend.rbac'
    verbose_name = 'RBAC'
