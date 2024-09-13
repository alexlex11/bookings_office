from django.http import HttpResponse
from rest_framework import viewsets, mixins
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime

from .models import MeetingRoom, Booking
from .serializers import MeetingRoomSerializer, UserSerializer, BookingSerializer, SignupSerializer, get_user_model
from .utils import ReportGenerator


class ReportViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=['get'], url_path=r'(?P<date_from>\d{4}-\d{2}-\d{2})-(?P<date_to>\d{4}-\d{2}-\d{2})')
    def report_by(self, request, date_from, date_to):
        start_date = date_from
        end_date = date_to

        bookings = Booking.objects.filter(start_datetime__gte=start_date, end_datetime__lte=end_date).order_by('start_datetime')
        
        report = ReportGenerator().create_report(bookings)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'attachment; filename=booking_report_{start_date}-{end_date}.docx'
        report.save(response)
        return response
    
class BookingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(detail=False, methods=['get'], url_path=r'today/(?P<room_id>\w+)',)
    def today(self, request, room_id):
        bookings = Booking.objects.filter(start_datetime__date=timezone.now().date()).filter(
            meeting_room__id=room_id).order_by('start_datetime')
        serializer = self.get_serializer(bookings, many=True)
        
        is_free = True
        for booking in serializer.data:
            start = booking['start_datetime']
            end = booking['end_datetime']
            current = timezone.now()
            if datetime.fromisoformat(start) <= current <= datetime.fromisoformat(end):
                is_free = False
                break

        return Response({'is_free': is_free, 'bookings': serializer.data})


class MeetingRoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignUpUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = SignupSerializer
