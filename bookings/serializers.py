from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from rest_framework import serializers


from bookings.models import MeetingRoom, Booking


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ('url', 'id', 'name', 'descriptions')


class UserSerializer(serializers.ModelSerializer):
    bookings = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Booking.objects.all())

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'bookings')


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Booking
        fields = ('url', 'id', 'meeting_room', 'user', 'descriptions',
                  'start_datetime', 'end_datetime', 'created_at')

    def validate(self, data):
        start_time = data['start_datetime']
        end_time = data['end_datetime']

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be greater than start time.")
        
        room_id = data['meeting_room'].id
        overlapped_bookings = Booking.objects.filter(meeting_room_id=room_id).filter(
            Q(start_datetime__lte=start_time, end_datetime__gte=start_time) |
            Q(start_datetime__lte=end_time, end_datetime__gte=end_time)
        )
        
        if overlapped_bookings.exists():
            raise serializers.ValidationError("The meeting room is already booked during that time.")

        return data
    
    def create(self, validated_data):
        booking = Booking(**validated_data,
                          user=self.context['request'].user
                          )
        booking.save()
        return booking


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
