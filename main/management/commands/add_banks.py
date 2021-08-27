
import requests, os
from ...models import Bank
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    
    
    def handle(self, *args, **options):
        res = requests.get('https://api.paystack.co/bank',headers={
            'Authorization':f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}"
        })

        data = res.json()['data']

        for d in data:
            if not d['is_deleted'] and d['active']:
                bank = Bank.objects.create(bank_name=d['name'], paystack_code=d['code'])
                self.stdout.write(self.style.SUCCESS(f"{bank.bank_name} added"))
