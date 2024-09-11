from rest_framework import serializers


from bookings.models import MeetingRoom, Booking


class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ('url', 'name', 'descriptions')