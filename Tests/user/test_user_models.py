import pytest

from user.models import (
    Client,
)

@pytest.mark.django_db
def test_client(client):
    assert isinstance(client, Client)
    assert str(client) == f"{client.name} - {client.stock.sector.name} - {client.stock.sector.public_defense.name}"