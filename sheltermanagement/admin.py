from django.contrib import admin
from .models import Shelter, Room, Bed, Guest, Booking

# Register your models here.
admin.site.register(Shelter)
admin.site.register(Room)
admin.site.register(Bed)
admin.site.register(Guest)
admin.site.register(Booking)
