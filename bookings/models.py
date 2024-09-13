from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class MeetingRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    descriptions = models.TextField(blank=True, null=True)


    def __str__(self):
        return f'{self.name}'


class Booking(models.Model):
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='bookings', on_delete=models.CASCADE)
    descriptions = models.TextField(blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} booked a {self.meeting_room} \nfrom {str(self.start_datetime)[:19]} to {str(self.end_datetime)[:19]} \nfor {self.descriptions} \nin {str(self.created_at)[:19]}.'

    class Meta:
        ordering = ['start_datetime']
