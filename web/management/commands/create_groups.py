from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Create admin and staff groups"

    def handle(self, *args, **kwargs):
        admin = Group.objects.get(name='admin')
        staff = Group.objects.get(name='staff')
        if not admin and not staff:
            Group.objects.create(name="admin")
            Group.objects.create(name="staff")

            self.stdout.write(self.style.SUCCESS('Successfully created groups admin and staff'))
        
        else:
            self.stdout.write(self.style.ERROR('Groups already exsist'))