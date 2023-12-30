from rest_framework import serializers
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id',
            'resource_name',
            'latitude',
            'longitude',
            'location_type',
            'address',
            'description',
            'hours'
        ]
