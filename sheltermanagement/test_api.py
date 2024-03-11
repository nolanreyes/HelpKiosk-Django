from django.test import TestCase
from .models import Shelter, Room, Bed, Booking
from .utils import handle_new_booking_event  # Adjust the import path as necessary


class BookingProcessTests(TestCase):
    def setUp(self):
        shelter = Shelter.objects.create(name="Test Shelter", location="POINT(0 0)", contact_info="Test Info")
        room_male = Room.objects.create(shelter=shelter, room_number="101", capacity=2,
                                        gender_allocation=Room.Gender.MALE, is_full=False)
        Bed.objects.create(room=room_male, bed_number="1", is_occupied=False)
        Bed.objects.create(room=room_male, bed_number="2", is_occupied=False)
        # Setup more rooms and beds as necessary

    def test_handle_new_booking_event(self):
        booking_data = {
            'gender': Room.Gender.MALE,
            'check_in_date': '2023-01-01',
            'check_out_date': '2023-01-05',
        }
        success, message = handle_new_booking_event(booking_data)
        self.assertTrue(success)  # Check if the booking was successful
        self.assertEqual(message, "Booking successful.")

        booking = Booking.objects.latest('id')
        print(f"New booking details: Room {booking.bed.room.room_number}, Bed {booking.bed.bed_number}, Check-in {booking.check_in_date}, Check-out {booking.check_out_date}")
        self.assertTrue(Booking.objects.exists(), "No Booking was created")
        occupied_beds = Bed.objects.filter(is_occupied=True)
        self.assertEqual(occupied_beds.count(), 1, "A bed should be marked as occupied")
