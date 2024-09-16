from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import MeetingRoom, Booking
from .serializers import MeetingRoomSerializer, ReportSerializer, BookingSerializer, SignupSerializer, get_user_model


@extend_schema_view(
    report_by=extend_schema(
        summary="Получить отчет в формате word, содержащий в себе данные за определенный период о бронированиях переговорных комнат",
    ))
class ReportViewSet(viewsets.GenericViewSet):
    serializer_class = ReportSerializer

    @action(detail=False, methods=['get'], url_path=r'(?P<date_from>\d{4}-\d{2}-\d{2})-(?P<date_to>\d{4}-\d{2}-\d{2})')
    def report_by(self, request, date_from, date_to):
        serializer = self.get_serializer(
            data={'date_from': date_from, 'date_to': date_to})
        serializer.is_valid(raise_exception=True)
        return serializer.to_representation(serializer.validated_data)


@extend_schema_view(
    list=extend_schema(
        summary="Получить все записи о бронировании",
    ),

    create=extend_schema(
        summary="Создание новой записи бронирования",
        request=BookingSerializer,
    ),
    retrieve=extend_schema(
        summary='Получить запись о бронирование по ID'
    ),
    today=extend_schema(
        summary='Получить все записи о бронировании переговорной комнаты по ID на текущий день'
    )
)
class BookingViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(detail=False, methods=['get'], url_path=r'today/(?P<room_id>\d+)',)
    def today(self, request, room_id):
        meeting_room = get_object_or_404(MeetingRoom, pk=room_id)
        today = timezone.now().date()
        bookings = Booking.objects.filter(
            meeting_room=meeting_room,
            start_datetime__date=today,
            end_datetime__date=today
        )
        serializer = self.get_serializer(bookings, many=True)

        is_free = True
        for booking in bookings:
            start = booking.start_datetime
            end = booking.end_datetime
            current = timezone.now()
            if start <= current <= end:
                is_free = False
                break

        return Response({'is_free': is_free, 'bookings': serializer.data})


@extend_schema_view(
    list=extend_schema(
        summary="Получить список существующих переговорных комнат",
    ),
    retrieve=extend_schema(
        summary='Детальная информация о переговорной комнате по ID'
    ))
class MeetingRoomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


@extend_schema_view(
    create=extend_schema(
        summary="Создание нового пользователя",
        description="Чтобы залогиниться вверху есть кнопка Authorize"
    ))
class SignUpUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()
    serializer_class = SignupSerializer
