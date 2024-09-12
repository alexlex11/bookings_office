from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated


from .models import MeetingRoom, Booking
from .serializers import MeetingRoomSerializer, UserSerializer, BookingSerializer, SignupSerializer, get_user_model


class MeetingRoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class SignUpUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = SignupSerializer
