# Generated by Django 3.2.2 on 2021-10-25 12:18

import account.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=250, verbose_name='first name')),
                ('last_name', models.CharField(max_length=250, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('phone', models.CharField(max_length=20, verbose_name='phone')),
                ('date_of_birth', models.CharField(max_length=20, verbose_name='date_of_birth')),
                ('gender', models.CharField(max_length=20, verbose_name='gender')),
                ('nationality', models.CharField(max_length=100, verbose_name='nationality')),
                ('address', models.CharField(max_length=400, verbose_name='address')),
                ('state_of_residence', models.CharField(max_length=100, verbose_name='state_of_residence')),
                ('education', models.CharField(max_length=400, verbose_name='education')),
                ('course', models.CharField(max_length=400, verbose_name='course')),
                ('currently_working', models.BooleanField(verbose_name='currently_working')),
                ('programing_experience', models.CharField(max_length=400, verbose_name='programing_experience')),
                ('own_laptop', models.BooleanField(verbose_name='own_laptop')),
                ('how_did_you_hear_about_us', models.CharField(max_length=400, verbose_name='how_did_you_hear_about_us')),
                ('password', models.CharField(max_length=500, verbose_name='password')),
                ('uploaded_id_url', models.CharField(max_length=300, null=True, verbose_name='profile picture url')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff')),
                ('is_admin', models.BooleanField(default=False, verbose_name='admin')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('auth_provider', models.CharField(default='email', max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', account.managers.UserManager()),
            ],
        ),
    ]