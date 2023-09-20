import pytest_asyncio
from httpx import AsyncClient
from main import app
from models import TechnicianRequests, CleaningRequests, MaidRequests
import uuid
from db import SessionLocal
from datetime import datetime
from dateutil.parser import parse

@pytest_asyncio.fixture
async def client():
    client = AsyncClient(app=app, base_url="http://127.0.0.1:8000")
    try:
        yield client
    finally:
        await client.aclose()

async def test_get_workorders_requests_maid_supervisor(client):
    response = await client.get("/workorders/mdsp01/workorder_requests")
    assert response.status_code == 200

async def test_get_workorders_requests_supervisor(client):
    response = await client.get("/workorders/sup001/workorder_requests")
    assert response.status_code == 200

cleaning_request_order_number = str(uuid.uuid4())
maid_request_order_number = str(uuid.uuid4())
technician_request_order_number = str(uuid.uuid4())


async def test_create_cleaning_request(client):
    # pdb.set_trace()
    response = await client.post(
        "/workorders/MDSP01/cleaning_requests",
        data={
            "order_number": cleaning_request_order_number,
            "created_by": "TMDSP01",
            "room_number": "T001",
            "started_at": "2023-08-29T10:00:00",
            "finished_at": "2023-08-29T12:00:00",
            "assigned_to": "TCLN01",
            "status": "created"
        }
    )
    assert response.status_code == 200

async def test_create_maid_request(client):
    response =  await client.post(
        "/workorders/MDSP01/maid_requests",
        data={
            "order_number": maid_request_order_number,
            "created_by": "TMDSP01",
            "assigned_to": "TMD01",
            "room_number": "T001",
            "started_at": "2023-09-23T10:00:00",
            "finished_at": "2023-09-23T12:00:00",
            "description": "Clean the room",
            "status": "created"
        }
    )
    assert response.status_code == 200

async def test_create_technician_request(client):
    response = await client.post(
        "/workorders/SUP001/technician_requests",
        data={
            "order_number": technician_request_order_number,
            "created_by": "TSUP01",
            "room_number": "T001",
            "defect_type": "Plumbing",
            "status": "created"
        }
    )
    assert response.status_code == 200

async def test_create_amenity_request(client):
    response = await client.post(
        "/workorders/1603951979670820/amenity_requests",
        data={
            "order_number": str(uuid.uuid4()),
            "created_by": 1603951979670820,
            "room_number": "T001",
            "amenity_type": "Towel",
            "quantity": 2,
        }
    )
    assert response.status_code == 200