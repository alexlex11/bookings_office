from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from bookings import views

urlpatterns = [
    path('meeting_rooms/', views.MeetingRoomList.as_view()),
    path('meeting_rooms/<int:pk>', views.MeetingRoomDetail.as_view()),
]

