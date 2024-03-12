from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Shelter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.PointField(help_text=_("Geographic location of the shelter"))
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name="rooms")
    room_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()
    gender_allocation = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('X', 'Mixed')])
    is_full = models.BooleanField(default=False)

    def __str__(self):
        return f"Room {self.room_number} in {self.shelter.name}"

    def occupied_beds_count(self):
        return self.beds.filter(is_occupied=True).count()

    def occupancy(self):
        return f"{self.occupied_beds_count()}/{self.capacity}"


class Bed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default=False)
    guest = models.OneToOneField('Guest', on_delete=models.SET_NULL, null=True, blank=True, related_name='bed')

    def __str__(self):
        return f"{self.room.shelter.name} - Room {self.room.room_number} - Bed {self.bed_number}"


class Guest(models.Model):
    wallet_address = models.CharField(max_length=42, unique=True)
    gender = models.CharField(max_length=1, choices=[('M', _('Male')), ('F', _('Female')), ('O', _('Other'))],
                              blank=True)

    def __str__(self):
        return self.wallet_address


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name="bookings")
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
