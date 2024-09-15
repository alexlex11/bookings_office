from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import serializers


from .utils import ReportGenerator
from bookings.models import MeetingRoom, Booking


class ReportSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=True)
    date_to = serializers.DateField(required=True)

    def to_representation(self, instance):
        start_date = instance['date_from']
        end_date = instance['date_to']

        bookings = Booking.objects.filter(
            start_datetime__gte=start_date, end_datetime__lte=end_date).order_by('start_datetime')

        report = ReportGenerator().create_report(bookings)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=booking_report_{
            start_date}-{end_date}.docx'
        report.save(response)
        return response


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ('url', 'id', 'name', 'descriptions')


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())
    meeting_room = MeetingRoomSerializer(read_only=True)
    meeting_room_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ('url', 'id', 'meeting_room', 'meeting_room_id', 'user', 'descriptions',
                  'start_datetime', 'end_datetime', 'created_at')

    def validate(self, data):
        start_time = data['start_datetime']
        end_time = data['end_datetime']

        if start_time >= end_time:
            raise serializers.ValidationError(
                "End time must be greater than start time.")

        room_id = data['meeting_room_id']
        overlapped_bookings = Booking.objects.filter(meeting_room_id=room_id).filter(
            Q(start_datetime__lte=start_time, end_datetime__gte=start_time) |
            Q(start_datetime__lte=end_time, end_datetime__gte=end_time)
        )

        if overlapped_bookings.exists():
            raise serializers.ValidationError(
                "The meeting room is already booked during that time.")

        return data

    def create(self, validated_data):
        meeting_room_id = validated_data.pop('meeting_room_id')
        booking = Booking(**validated_data,
                          user=self.context['request'].user,
                          meeting_room=MeetingRoom.objects.get(
                              pk=meeting_room_id)
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
