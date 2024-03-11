from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class Shelter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.PointField(help_text=_("Geographic location of the shelter"))
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Room(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        MIXED = 'X', _('Mixed')
        NONE = 'N', _('None')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shelter = models.ForeignKey(Shelter, on_delete=models.CASCADE, related_name="rooms")
    room_number = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()
    gender_allocation = models.CharField(max_length=1, choices=Gender.choices, default=Gender.NONE)
    is_full = models.BooleanField(default=False)

    def __str__(self):
        return f"Room {self.room_number} in {self.shelter.name}"


class Bed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default=False)
    special_features = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.room.shelter.name} - Room {self.room.room_number} - Bed {self.bed_number}"


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, related_name="bookings")
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
