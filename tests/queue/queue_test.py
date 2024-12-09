import pytest
from fastapi.testclient import TestClient
from app.main import app  # Adjust to your app's entry point

client = TestClient(app)

def test_queue_endpoint():
    payload = {"text": "Sample string"}
    response = client.post("/queue", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully added to queue"}  # Adjust based on your response
