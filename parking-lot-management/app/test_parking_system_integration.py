import pytest
import uuid
from unittest.mock import patch, MagicMock
import parking_system

@pytest.fixture
def client():
    parking_system.app.config['TESTING'] = True
    with parking_system.app.test_client() as client:
        yield client


def get_random_plate():
    return str(uuid.uuid4())[:8]


def test_vehicle_entry_duplicate(client):
    response = client.post('/entry', query_string={'plate': 'check', 'parkingLot': 'parkingLot'})
    response = client.post('/entry', query_string={'plate': 'check', 'parkingLot': 'parkingLot'})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Plate already exists'

def test_vehicle_entry_success(client):
    random_plate = get_random_plate()
    response = client.post('/entry', query_string={'plate': random_plate, 'parkingLot': 'parkingLot'})
    assert response.status_code == 200
    assert 'ticketId' in response.get_json()

def test_vehicle_entry_missing_parkingLot(client):
    random_plate = get_random_plate()
    response = client.post('/entry', query_string={'plate': random_plate})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Missing parkingLot parameter'

def test_vehicle_entry_missing_plate(client):
    response = client.post('/entry', query_string={'parkingLot': 'parkingLot'})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Missing plate parameter'

def test_vehicle_exit_success(client):
    plate = get_random_plate()
    print(plate)
    response = client.post('/entry', query_string={'plate': plate, 'parkingLot': 'parkingLot'})
    print(response)
    ticket = response.get_json()['ticketId']
    print(plate)
    response = client.post('/exit', query_string={'ticketId': ticket})
    assert response.status_code == 200
    data = response.get_json()
    assert data['plate'] == plate
    assert data['parkingLot'] == 'parkingLot'
    assert 'parkedTimeMinutes' in data
    assert 'fee' in data

def test_vehicle_exit_missing_ticket_id(client):
    response = client.post('/exit')
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Missing ticketId'

def test_vehicle_exit_invalid_ticket_id(client):
    response = client.post('/exit', query_string={'ticketId': '123'})
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Invalid ticketId'


