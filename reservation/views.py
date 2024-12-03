from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Seat
import json

@csrf_exempt
def reserve_seats(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            num_seats = data.get('numSeats')
            booked_by = data.get('bookedBy')

            if num_seats > 7:
                return JsonResponse({'error': 'Cannot reserve more than 7 seats at a time'}, status=400)

            available_seats_count = Seat.objects.filter(isReserved=False).count()

            if available_seats_count < num_seats:
                return JsonResponse({'error': f'Only {available_seats_count} seats available, cannot reserve {num_seats} seats'}, status=400)

            # Reserve seats logic
            reserved_seats = []
            rows = Seat.objects.filter(isReserved=False).values('rowNumber').annotate(count=models.Count('id'))

            # Try to reserve in a single row if enough seats are available
            for row in rows:
                if row['count'] >= num_seats:
                    seats_in_row = Seat.objects.filter(rowNumber=row['rowNumber'], isReserved=False)[:num_seats]
                    reserved_seats = seats_in_row
                    break

            # If not enough seats in one row, reserve available seats across rows
            if not reserved_seats:
                reserved_seats = Seat.objects.filter(isReserved=False)[:num_seats]

            # Mark the seats as reserved
            reserved_seats.update(isReserved=True, bookedBy=booked_by)

            # Return reserved seat details
            reserved_seat_details = list(reserved_seats.values('rowNumber', 'seatNumber'))

            return JsonResponse({'success': True, 'reservedSeats': reserved_seat_details})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def seat_availability(request):
    try:
        available_seats_count = Seat.objects.filter(isReserved=False).count()
        booked_seats_count = Seat.objects.filter(isReserved=True).count()

        return JsonResponse({
            'availableSeatsCount': available_seats_count,
            'bookedSeatsCount': booked_seats_count
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_all_seats(request):
    try:
        seats = Seat.objects.all()
        seats_with_position = [{
            'CoachPosition': (7 * (seat.rowNumber - 1)) + seat.seatNumber,
            'isReserved': seat.isReserved
        } for seat in seats]

        return JsonResponse({'seats': seats_with_position})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
