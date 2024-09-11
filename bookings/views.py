from rest_framework import viewsets
from django.contrib.auth.models import User


from .models import MeetingRoom, Booking
from .serializers import MeetingRoomSerializer, UserSerializer, BookingSerializer


class MeetingRoomViewSet(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
