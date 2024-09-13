import pytest
from datetime import datetime, timedelta
from django.contrib.auth.models import User


from bookings.models import Booking, MeetingRoom


API_CREATE_BOOKING_URL = '/api/bookings/'
API_GET_ROOM_BOOKINGS_URL = '/api/bookings/today/'
API_REPORT_URL = '/api/reports/'

@pytest.mark.django_db
def test_create_booking_201(api_client):
    """
    Test the create booking API
    :param api_client:
    :return: None
    """
    test_meeting_room_name = 'test meeting room'
    MeetingRoom.objects.create(name=test_meeting_room_name,
                               descriptions='test description')

    start_datetime = datetime.today() + timedelta(days=1)
    end_datetime = datetime.today() + timedelta(days=2)

    payload = {
        "meeting_room_id": 1,
        "descriptions": "test booking description",
        "start_datetime": start_datetime,
        "end_datetime": end_datetime
    }

    test_user = User.objects.create_user(
        username='testusername', password='testpassword')
    api_client.force_login(test_user)

    response_create = api_client.post(
        API_CREATE_BOOKING_URL, data=payload, format='json')

    assert response_create.status_code == 201
    assert response_create.data['meeting_room']['id'] == payload['meeting_room_id']
    assert response_create.data["descriptions"] == payload["descriptions"]


@pytest.mark.django_db
def test_create_booking_400(api_client):
    """
    Test the create booking API
    :param api_client:
    :return: None
    """
    test_meeting_room_name = 'test meeting room'
    MeetingRoom.objects.create(name=test_meeting_room_name,
                               descriptions='test description')

    start_datetime = datetime.today() + timedelta(days=3)
    end_datetime = datetime.today() + timedelta(days=2)

    payload = {
        "meeting_room_id": 1,
        "descriptions": "test booking description",
        "start_datetime": start_datetime,
        "end_datetime": end_datetime
    }

    test_user = User.objects.create_user(
        username='testusername', password='testpassword')
    api_client.force_login(test_user)

    response_create = api_client.post(
        API_CREATE_BOOKING_URL, data=payload, format='json')

    assert response_create.status_code == 400


@pytest.mark.django_db
def test_get_room_bookings_is_not_free(api_client):
    """
    Test the get room bookings API
    :param api_client:
    :return: None
    """
    test_user = User.objects.create_user(
        username='testusername', password='testpassword')
    test_meeting_room_name = 'test meeting room'
    meeting_room = MeetingRoom.objects.create(name=test_meeting_room_name,
                                              descriptions='test description')

    api_client.force_login(test_user)
    response_get = api_client.get(
        f'{API_GET_ROOM_BOOKINGS_URL}1/', data={'room_id': 1}, format='json')

    assert response_get.data['is_free']

    today_start_datetime = datetime.now()
    today_end_datetime = datetime.now() + timedelta(hours=1)

    not_today_start_datetime = datetime.now() + timedelta(hours=2)
    not_today_end_datetime = datetime.now() + timedelta(hours=4)

    today_payload = {
        "meeting_room": meeting_room,
        "descriptions": "test booking description",
        "start_datetime": today_start_datetime,
        "end_datetime": today_end_datetime
    }

    not_today_payload = {
        "meeting_room": meeting_room,
        "descriptions": "test booking description",
        "start_datetime": not_today_start_datetime,
        "end_datetime": not_today_end_datetime
    }

    print(Booking.objects.create(**today_payload, user=test_user))
    print(Booking.objects.create(**not_today_payload, user=test_user))


    response_get = api_client.get(
         f'{API_GET_ROOM_BOOKINGS_URL}1/', data={'room_id': 1}, format='json')

    assert response_get.status_code == 200
    assert len(response_get.data['bookings']) != 0
    assert response_get.data['is_free'] == False


@pytest.mark.django_db
def test_get_room_bookings_is_free(api_client):
    """
    Test the get room bookings API
    :param api_client:
    :return: None
    """
    test_user = User.objects.create_user(
        username='testusername', password='testpassword')
    test_meeting_room_name = 'test meeting room'
    meeting_room = MeetingRoom.objects.create(name=test_meeting_room_name,
                                              descriptions='test description')

    api_client.force_login(test_user)
    response_get = api_client.get(
        f'{API_GET_ROOM_BOOKINGS_URL}1/', data={'room_id': 1}, format='json')


    assert response_get.status_code == 200
    assert len(response_get.data['bookings']) == 0
    assert response_get.data['is_free']


@pytest.mark.django_db
def test_report_200(api_client):
    """
    Test the get room bookings API
    :param api_client:
    :return: None
    """
    test_user = User.objects.create_user(
        username='testusername', password='testpassword')
    api_client.force_login(test_user)
    
    start_datetime = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')
    end_datetime = (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d')
    
    response_get = api_client.get(
        f'{API_REPORT_URL}{start_datetime}-{end_datetime}/', data={'date_from': str(start_datetime), 'date_to': str(end_datetime)}, format='json')


    assert response_get.status_code == 200
