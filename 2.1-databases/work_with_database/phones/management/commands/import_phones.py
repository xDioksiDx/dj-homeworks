import csv
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from phones.models import Phone


class Command(BaseCommand):
    help = "Import phones from CSV into database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--path",
            default=os.path.join(settings.BASE_DIR, "phones.csv"),
            help="Path to phones.csv (default: <BASE_DIR>/phones.csv)",
        )

    def handle(self, *args, **options):
        path = options["path"]

        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f"File not found: {path}"))
            return

        with open(path, "r", encoding="utf-8", newline="") as f:
            phones = csv.DictReader(f, delimiter=";")

            for phone in phones:
                Phone.objects.update_or_create(
                    id=int(phone["id"]),
                    defaults={
                        "name": phone["name"],
                        "image": phone["image"],
                        "price": float(phone["price"]),
                        "release_date": datetime.strptime(phone["release_date"], "%Y-%m-%d").date(),
                        "lte_exists": phone["lte_exists"].strip().lower() == "true",
                    },
                )

        self.stdout.write(self.style.SUCCESS("Phones imported successfully"))