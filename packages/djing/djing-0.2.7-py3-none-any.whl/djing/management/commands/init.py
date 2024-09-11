import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from djing.core.application import Application


class Command(BaseCommand):
    help = "Handles DJing resources like Post"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Force action even if conditions are met.",
        )

    def handle(self, *args, **options):
        try:
            force = options["force"]

            application: Application = getattr(settings, "application")

            DJING_PACKAGE_PATH = getattr(settings, "DJING_PACKAGE_PATH")

            template_dir = DJING_PACKAGE_PATH / "templates" / "djing_admin"

            if application.initialized and not force:
                raise self.stdout.write(
                    "Application is already initialized. Use --force to overwrite."
                )

            if application.admin_root.exists() and force:
                shutil.rmtree(application.admin_root)

            shutil.copytree(template_dir, application.admin_root)

            self.stdout.write("Application initialized successfully.")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
