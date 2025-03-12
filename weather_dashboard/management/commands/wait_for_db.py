import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for DB...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("DB is not ready yet, waiting 2 sec...")
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS("DB is ready!"))
