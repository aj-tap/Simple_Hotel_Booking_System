# Generated by Django 3.2.9 on 2021-12-15 05:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_of_birth', models.DateField(null=True)),
                ('phone', models.CharField(help_text='+63', max_length=12, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Guest List',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_num', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('checkin_date', models.DateTimeField(default=datetime.datetime(2021, 12, 15, 5, 21, 4, 767916))),
                ('checkout_date', models.DateTimeField(default=datetime.datetime(2021, 12, 16, 5, 21, 4, 767939))),
                ('check_out', models.BooleanField(default=False)),
                ('no_of_guests', models.IntegerField(default=1)),
                ('guest_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Booking List',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('hotel_code', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=12)),
                ('hotel_email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_no', models.IntegerField(default=101)),
                ('room_type', models.CharField(choices=[('Studio', 'Studio room'), ('standard', 'Standard room'), ('family', 'Family room')], default='standard', max_length=200)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_available', models.BooleanField(default=True)),
                ('no_of_beds', models.IntegerField(default=3)),
                ('description', models.CharField(max_length=100, null=True)),
                ('room_img', models.ImageField(null=True, upload_to='images')),
                ('hotel_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel_app.hotel')),
            ],
            options={
                'verbose_name': 'Hotel Room',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rating', models.CharField(max_length=12)),
                ('guest_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_owner', models.CharField(max_length=32, null=True)),
                ('card_number', models.IntegerField(max_length=16, null=True)),
                ('card_cvv', models.IntegerField(max_length=3, null=True)),
                ('exp_month', models.IntegerField(max_length=2, null=True)),
                ('exp_year', models.IntegerField(max_length=4, null=True)),
                ('booking_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_app.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='hotel_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel_app.hotel'),
        ),
        migrations.AddField(
            model_name='booking',
            name='room_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel_app.room'),
        ),
    ]
