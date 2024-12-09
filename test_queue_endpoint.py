import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# def test_create_queue_item():
#     # Define the payload for the POST request
#     payload = {
#         "user_id": 1,
#         "raw_text": "This is a test item.",
#         "options": {"priority": "high", "tags": ["test", "queue"]}
#     }

#     # Send the POST request to the /queue endpoint
#     response = client.post("/queue", json=payload)

#     # Check that the response status code is 200
#     assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

#     # Check that the response contains the queue_id
#     response_data = response.json()
#     assert "queue_id" in response_data, "Response does not contain 'queue_id'"
#     assert isinstance(response_data["queue_id"], int), "queue_id is not an integer"

def test_create_queue_item():
    # Define the payload for the POST request
    payload = {
        "user_id": 1,
        "raw_text": "This is a test item.",
        "options": {"priority": "high", "tags": ["test", "queue"]}
    }

    # Send the POST request to the /queue endpoint
    response = client.post("/queue", json=payload)

    # Print response for debugging
    print("Response status code:", response.status_code)
    print("Response body:", response.text)

    # Check that the response status code is 200
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

    # Check that the response contains the queue_id
    response_data = response.json()
    assert "queue_id" in response_data, "Response does not contain 'queue_id'"
    assert isinstance(response_data["queue_id"], int), "queue_id is not an integer"


if __name__ == "__main__":
    pytest.main()
