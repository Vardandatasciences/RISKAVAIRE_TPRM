"""
Django management command to fix foreign key constraints
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fix foreign key constraints to allow migrations'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                # Disable foreign key checks
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                self.stdout.write("[EMOJI] Disabled foreign key checks")
                
                # Try to drop problematic tables if they exist
                try:
                    cursor.execute("DROP TABLE IF EXISTS vendors")
                    self.stdout.write("[EMOJI] Dropped vendors table")
                except Exception as e:
                    self.stdout.write(f"[EMOJI]  Could not drop vendors table: {e}")
                
                try:
                    cursor.execute("DROP TABLE IF EXISTS vendor_categories")
                    self.stdout.write("[EMOJI] Dropped vendor_categories table")
                except Exception as e:
                    self.stdout.write(f"[EMOJI]  Could not drop vendor_categories table: {e}")
                
                # Re-enable foreign key checks
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                self.stdout.write("[EMOJI] Re-enabled foreign key checks")
                
                self.stdout.write(self.style.SUCCESS('[EMOJI] Foreign key constraints fixed successfully!'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[EMOJI] Error fixing foreign keys: {e}'))
                raise
