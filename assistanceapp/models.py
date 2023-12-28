from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    resource_name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

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