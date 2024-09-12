from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bookings import views

router = DefaultRouter()
router.register(r'meeting-rooms', views.MeetingRoomViewSet, 'meetingroom')
router.register(r'users', views.UserViewSet, 'user')
router.register(r'sing-up', views.SignUpUserView, 'singup')
router.register(r'bookings', views.BookingViewSet, 'booking')

urlpatterns = [
    path('', include(router.urls)),
]
