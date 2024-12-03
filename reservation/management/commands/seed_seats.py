from django.core.management.base import BaseCommand
from reservation.models import Seat

class Command(BaseCommand):
    help = 'Seeds the database with seat data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding the seats data...'))

        # Clear existing seats
        Seat.objects.all().delete()

        # Create new seats (11 rows of 7 seats and 1 row of 3 seats)
        seats = []
        for row in range(1, 13):
            seats_in_row = 3 if row == 12 else 7
            for seat in range(1, seats_in_row + 1):
                seats.append(Seat(rowNumber=row, seatNumber=seat))

        # Insert the seats into the database
        Seat.objects.bulk_create(seats)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the seats data'))
