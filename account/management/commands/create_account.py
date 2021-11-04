from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
import csv
import string
import random

User=get_user_model()



class Command(BaseCommand):
    def handle(self, *args, **options):
        # User.objects.filter(is_staff=False, is_admin=False).delete()
        with open('account/management/commands/user_data.csv', mode='r', encoding='UTF-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            # line_count = 0
            for row in csv_reader:
                lower = string.ascii_lowercase
                upper = string.ascii_uppercase
                num = string.digits
                symbols = "!@#=$"
                all = lower + upper + num + symbols
                password = "".join(random.sample(all,8))
                row['password'] = password
                if User.objects.filter(email=row['email'], is_active=True).exists():
                    continue
                else:
                    user = User.objects.create(**row)
                    user.set_password(password)
                    user.save()

