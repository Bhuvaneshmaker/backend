from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"


class Command(BaseCommand):
    help = "Ensure the default admin user exists for mobile sign-in."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username=DEFAULT_USERNAME,
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        if not user.email:
            user.email = "admin@example.com"
        user.set_password(DEFAULT_PASSWORD)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created default admin user '{DEFAULT_USERNAME}' with password '{DEFAULT_PASSWORD}'."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Reset password for existing user '{DEFAULT_USERNAME}' to '{DEFAULT_PASSWORD}'."
                )
            )
