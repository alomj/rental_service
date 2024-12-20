# Generated by Django 5.1.2 on 2024-11-11 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0003_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('rental_start_date', models.DateField()),
                ('rental_end_date', models.DateField()),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_insurance_included', models.BooleanField(default=False)),
                ('mileage_limit', models.IntegerField(blank=True, null=True)),
                ('special_requirements', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airline', models.CharField(max_length=100)),
                ('flight_number', models.CharField(max_length=50)),
                ('date_of_departure', models.DateField()),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('place_of_departure', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('seat_class', models.CharField(max_length=50)),
                ('is_direct', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('date_of_arrival', models.DateField()),
                ('departure_date', models.DateField()),
                ('room_type', models.CharField(max_length=100)),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('number_of_guests', models.IntegerField()),
                ('is_breakfast_included', models.BooleanField(default=False)),
                ('special_requests', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('CANCELLED', 'Cancelled'), ('COMPLETED', 'Completed')], default='ACTIVE', max_length=10)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.car')),
                ('flight', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.flight')),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='booking.hotel')),
            ],
        ),
    ]
