import os
import csv
import pytest
import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com/posts"
TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "test_data.csv")


def read_test_data():
    """Read CSV test data"""
    data_list = []
    with open(TEST_DATA_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_list.append(row)
    return data_list


@pytest.mark.parametrize("data", read_test_data())
def test_create_posts(data):
    """POST request test"""

    tc_no = data["tc_no"].strip()
    tc_name = data.get("tc_name", f"TestCase_{tc_no}")
    user_id = data["userId"].strip()
    title = data["title"].strip()
    body = data["body"].strip()
    expected_status = int(data["post_status_code"].strip())

    # ---- Request Payload ----
    payload = {
        "userId": int(user_id),
        "title": title,
        "body": body
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "pytest-automation-client"
    }

    # ---- Send POST Request ----
    response = requests.post(BASE_URL, headers=headers, json=payload)

    print(f"\n{'=' * 100}")
    print(f"Test Case: {tc_no} - {tc_name}")

    print("\nRequest:")
    print(f"\nURL: {BASE_URL}")

    # ---- Request Headers ----
    print("\nRequest Headers:")
    for key, value in response.request.headers.items():
        print(f"{key}: {value}")

    # ---- Request Body ----
    print("\nRequest Body:")
    print(json.dumps(payload, indent=2))

    print(f"{'=' * 100}")

    print("\nResponse:")
    print(f"\nExpected Status: {expected_status}, Actual: {response.status_code}")
    # ---- Response Headers ----
    print("\nResponse Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

    # ---- Response Body ----
    print("\nResponse Body:")
    try:
        print(json.dumps(response.json(), indent=4))
    except ValueError:
        print(response.text)

    # ---- Assertions ----
    assert response.status_code == expected_status, (
        f"FAILED: Expected {expected_status}, got {response.status_code}"
    )

