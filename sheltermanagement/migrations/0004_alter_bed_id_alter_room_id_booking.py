# Generated by Django 5.0 on 2024-03-05 03:34

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheltermanagement', '0003_alter_room_id_bed_delete_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bed',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('check_in_date', models.DateField()),
                ('check_out_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='sheltermanagement.bed')),
            ],
        ),
    ]