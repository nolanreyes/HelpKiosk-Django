from django.contrib.gis import admin
from .models import Location


class LocationAdmin(admin.GISModelAdmin):
    admin.site.register(Location, admin.GISModelAdmin)
