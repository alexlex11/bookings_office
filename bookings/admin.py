from django.contrib import admin


from .models import Booking, MeetingRoom


admin.site.register(MeetingRoom)
admin.site.register(Booking)
