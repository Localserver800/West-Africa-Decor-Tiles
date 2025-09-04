from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Lists all superusers'

    def handle(self, *args, **options):
        superusers = CustomUser.objects.filter(is_superuser=True)
        if superusers:
            self.stdout.write(self.style.SUCCESS('Superusers:'))
            for user in superusers:
                self.stdout.write(user.username)
        else:
            self.stdout.write(self.style.WARNING('No superusers found.'))
