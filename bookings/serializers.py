from django.contrib.auth.models import User
from rest_framework import serializers


from bookings.models import MeetingRoom, Booking


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ('url', 'name', 'descriptions')


class UserSerializer(serializers.ModelSerializer):
    bookings = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Booking.objects.all())

    class Meta:
        model = User
        fields = ('url', 'username', 'bookings')


class BookingSerializer(serializers.ModelSerializer):
    meeting_room = MeetingRoomSerializer(read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ('url', 'meeting_room', 'user', 'descriptions',
                  'start_datetime', 'end_datetime', 'is_free', 'created_at')
