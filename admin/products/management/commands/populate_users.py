from django.core.management.base import BaseCommand
from products.models import User


class Command(BaseCommand):
    help = 'Populate the database with 10 sample users'

    def handle(self, *args, **options):
        # Create 10 users
        for i in range(1, 11):
            user = User.objects.create()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created user {i}')
            )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with 10 users')
        )
