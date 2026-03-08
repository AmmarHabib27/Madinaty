import getpass
from django.core.management.base import BaseCommand
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Create a new admin account.'

    def add_arguments(self, parser):
        parser.add_argument('--phone', type=str, help='Admin phone number')
        parser.add_argument('--name', type=str, help='Admin name')
        parser.add_argument('--password', type=str, help='Admin password')

    def handle(self, *args, **options):
        from base.models import Admin

        phone = options.get('phone') or input('Phone: ').strip()
        name = options.get('name') or input('Name: ').strip()

        if not phone:
            self.stderr.write('Phone is required.')
            return

        if not name:
            self.stderr.write('Name is required.')
            return

        if Admin.objects.filter(phone=phone).exists():
            self.stderr.write(f'An admin with phone "{phone}" already exists.')
            return

        password = options.get('password')
        while not password:
            password = getpass.getpass('Password: ')
            confirm = getpass.getpass('Password (again): ')
            if password != confirm:
                self.stderr.write('Passwords do not match. Try again.')
                password = None
                continue
            try:
                validate_password(password)
            except ValidationError as e:
                for error in e.messages:
                    self.stderr.write(error)
                bypass = input('Bypass password validation and create admin anyway? [y/N]: ').strip().lower()
                if bypass != 'y':
                    password = None

        Admin.objects.create_admin(phone=phone, name=name, password=password)
        self.stdout.write(self.style.SUCCESS(f'Admin "{name}" ({phone}) created successfully.'))
