import shutil

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
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

            # Access the application and DJING_PACKAGE_PATH from settings
            application: Application = getattr(settings, "application")
            DJING_PACKAGE_PATH = getattr(settings, "DJING_PACKAGE_PATH")

            # Define the paths for template and application directories
            template_dir = DJING_PACKAGE_PATH / "templates" / "djing_admin"
            admin_root = application.admin_root

            # Check if application is already initialized
            if application.initialized and not force:
                raise CommandError(
                    "Application is already initialized. Use --force to overwrite."
                )

            # Remove existing admin_root directory if force is used
            if admin_root.exists() and force:
                shutil.rmtree(admin_root)

            # Copy the template directory to the admin_root
            shutil.copytree(template_dir, admin_root)

            # Output success message
            self.stdout.write(
                self.style.SUCCESS("Application initialized successfully.")
            )

        except:
            raise
