from django.db import models

# Create your models here.
class Seat(models.Model):
    rowNumber = models.IntegerField()        # The row number (1-12)
    seatNumber = models.IntegerField()       # The seat number (1-7 or 1-3 in the last row)
    isReserved = models.BooleanField(default=False)  # Whether the seat is reserved or not
    bookedBy = models.CharField(max_length=255, null=True, blank=True)  # Name of the person who reserved the seat (nullable)

    def __str__(self):
        return f"Row {self.rowNumber} - Seat {self.seatNumber}"

