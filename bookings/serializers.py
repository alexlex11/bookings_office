from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
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

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password', ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = get_user_model()(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user