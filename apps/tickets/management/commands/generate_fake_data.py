from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from apps.tickets.models import Ticket
from apps.tickets.choices import StatusChoices

User = get_user_model()

class Command(BaseCommand):
    help = 'Generates fake data for testing'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create fake users
        self.stdout.write(self.style.SUCCESS('Creating fake users...'))
        for i in range(1, 11):  # Create 10 fake users
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'
            )
            self.stdout.write(self.style.SUCCESS(f'#{i}-Created user: {user.username}'))

        # Create fake tickets
        self.stdout.write(self.style.SUCCESS('Creating fake tickets...'))
        users = User.objects.all()
        for _ in range(50):  # Create 50 fake tickets
            ticket = Ticket.objects.create(
                title=fake.sentence(),
                description=fake.paragraph(),
                status=fake.random_element(elements=StatusChoices.choices)[0],
                assigned_to=fake.random_element(elements=users) if fake.boolean() else None
            )
            self.stdout.write(self.style.SUCCESS(f'Created ticket: {ticket.title}'))

        self.stdout.write(self.style.SUCCESS('Fake data generation complete!'))