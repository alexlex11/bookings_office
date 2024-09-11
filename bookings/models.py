from django.db import models
from django.contrib.auth.models import User


class MeetingRoom(models.Model):
    name = models.CharField(max_length=255)
    descriptions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}: {self.descriptions}'


class Booking(models.Model):
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descriptions = models.TextField(blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    is_free = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} booked a {self.meeting_room} from {self.start_datetime} to {self.end_datetime} for {self.descriptions}.'

    class Meta:
        ordering = ['created_at']
