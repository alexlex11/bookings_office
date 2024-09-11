from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookings import views

router = DefaultRouter()
router.register(r'meeting_rooms', views.MeetingRoomViewSet, 'meeting room')
router.register(r'users', views.UserViewSet, 'users')
router.register(r'bookings', views.BookingViewSet, 'bookings')

urlpatterns = [
    path('', include(router.urls)),
]
