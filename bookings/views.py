from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import MeetingRoom, Booking
from .serializers import MeetingRoomSerializer, UserSerializer, BookingSerializer, SignupSerializer, get_user_model


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(detail=False, methods=['get'])
    def today(self, request):
        bookings = Booking.objects.filter(start_datetime__date=timezone.now())
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
        

class MeetingRoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignUpUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = SignupSerializer
