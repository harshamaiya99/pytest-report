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
def test_posts(data):

    post_id = data["post_id"].strip()
    expected_status = int(data["expected_status"])

    # Build full URL
    url = f"{BASE_URL}/{post_id}" if post_id else BASE_URL

    headers = {
        "Accept": "application/json",
        "User-Agent": "pytest-automation-client"
    }

    # Optionally support POST or PATCH later
    response = requests.get(url, headers=headers)

    print(f"\n{'=' * 100}")
    print(f"Test: {data['test_name']}")
    print(f"URL: {url}")
    print(f"Expected Status: {expected_status}, Actual: {response.status_code}")
    print(f"{'=' * 100}\n")

    # ---- Request Headers ----
    print("Request Headers:")
    for key, value in response.request.headers.items():
        print(f"{key}: {value}")

    # ---- Request Body (if present) ----
    if response.request.body:
        print("\nRequest Body:")
        try:
            print(json.dumps(json.loads(response.request.body), indent=2))
        except Exception:
            print(response.request.body)

    print(f"{'=' * 100}\n")

    # ---- Response Headers ----
    print("\nResponse Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")

    # ---- Response Body (if present) ----
    if response.text.strip():
        print("\nResponse Body:")
        try:
            print(json.dumps(response.json(), indent=2))
        except ValueError:
            print(response.text)

    # ---- Assertion ----
    assert response.status_code == expected_status, (
        f"FAILED: Expected {expected_status}, got {response.status_code}"
    )
