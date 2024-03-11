from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    TYPE_CHOICES = [
        ('SHELTER', 'Shelter'),
        ('FOOD', 'Food'),
        ('HEALTH', 'Health Services'),
        ('HYGIENE', 'Hygiene'),
        ('LEGAL', 'Legal'),
        ('WIFI', 'Wifi'),
        ('OTHER', 'Other'),
    ]

    resource_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='OTHER')
    address = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    hours = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'location'

    def __str__(self):
        return self.resource_name

    def save(self, *args, **kwargs):
        # Check if any duplicates before making new
        existing_location = Location.objects.filter(
            resource_name=self.resource_name,
            latitude=self.latitude,
            longitude=self.longitude
        ).first()

        if existing_location:
            # dont create if exists
            return

        super(Location, self).save(*args, **kwargs)
