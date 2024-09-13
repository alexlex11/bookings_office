import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_create_task(api_client):
    pass