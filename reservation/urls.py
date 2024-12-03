from django.urls import path
from . import views

urlpatterns = [
    path('reserve/', views.reserve_seats, name='reserve_seats'),
    path('availability/', views.seat_availability, name='seat_availability'),
    path('seats/', views.get_all_seats, name='get_all_seats'),
]
