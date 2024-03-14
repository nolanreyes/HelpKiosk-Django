# Generated by Django 5.0 on 2023-12-30 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistanceapp', '0005_alter_location_location_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_type',
            field=models.CharField(choices=[('SHELTER', 'Shelter'), ('FOOD', 'Food'), ('HEALTH', 'Health Services'), ('HYGIENE', 'Hygiene'), ('LEGAL', 'Legal'), ('WIFI', 'Wifi'), ('OTHER', 'Other')], default='OTHER', max_length=20),
        ),
    ]