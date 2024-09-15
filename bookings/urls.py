from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bookings import views

router = DefaultRouter()
router.register(r'meeting-rooms', views.MeetingRoomViewSet, 'meetingroom')
router.register(r'singup', views.SignUpUserView, 'singup')
router.register(r'bookings', views.BookingViewSet, 'booking')
router.register(r'reports', views.ReportViewSet, 'report')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
