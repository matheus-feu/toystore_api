import random

from django.core.management.base import BaseCommand
from faker import Faker

from toy_store.models.customer import Customer
from toy_store.models.sale import Sale


class Command(BaseCommand):
    """
    Comando para popular o banco de dados com clientes e vendas fake.

    Como usar:
        python manage.py seed_data
    """
    help = 'Popula o banco com clientes e vendas fake'

    def handle(self, *args, **kwargs):
        faker = Faker('pt_BR')
        customers = []
        for _ in range(20):
            customer = Customer.objects.create(
                name=faker.name(),
                email=faker.unique.email(),
                phone=faker.phone_number(),
                address=faker.address(),
                date_of_birth=faker.date_of_birth(minimum_age=18, maximum_age=70)
            )
            customers.append(customer)
        self.stdout.write(self.style.SUCCESS('Clientes criados!'))

        for customer in customers:
            for _ in range(random.randint(1, 10)):
                Sale.objects.create(
                    customer=customer,
                    total_amount=round(random.uniform(10, 500), 2),
                    sale_date=faker.date_time_this_year()
                )
        self.stdout.write(self.style.SUCCESS('Vendas criadas!'))
