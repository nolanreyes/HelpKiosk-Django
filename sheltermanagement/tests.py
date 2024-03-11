from django.test import TestCase
from django.contrib.gis.geos import Point
from .models import Shelter, Room



class AvailableRoomTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a shelter with a geographic location
        shelter_location = Point(1, 1)  # Example location
        shelter = Shelter.objects.create(
            name='Test Shelter',
            location=shelter_location,
            contact_info='Contact Info'
        )

        # Create rooms, some of which are marked as full
        Room.objects.create(shelter=shelter, room_number='101', capacity=2, is_full=False,
                            gender_allocation=Room.Gender.NONE)
        Room.objects.create(shelter=shelter, room_number='102', capacity=2, is_full=True,
                            gender_allocation=Room.Gender.MALE)
        Room.objects.create(shelter=shelter, room_number='103', capacity=3, is_full=False,
                            gender_allocation=Room.Gender.FEMALE)

    def test_show_available_rooms(self):
        available_rooms = Room.objects.filter(is_full=False)

        print("\nAvailable Rooms:")
        for room in available_rooms:
            print(
                f"Shelter: {room.shelter.name}, Room Number: {room.room_number}, Capacity: {room.capacity}, Gender Allocation: {room.get_gender_allocation_display()}")

        # Asserting that there are exactly 2 available rooms
        self.assertEqual(available_rooms.count(), 2)
