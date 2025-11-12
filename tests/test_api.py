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
    """Test /posts endpoint with full response details"""
    post_id = data["post_id"].strip()
    expected_status = int(data["expected_status"])

    # Build full URL
    url = f"{BASE_URL}/{post_id}" if post_id else BASE_URL

    # Example headers (customize if needed)
    headers = {
        "Accept": "application/json",
        "User-Agent": "pytest-automation-client"
    }

    response = requests.get(url, headers=headers)

    print(f"\nTest: {data['test_name']}")
    print(f"\nRequest:")
    print(f"URL: {url}")
    # print("\nRequest Headers:", json.dumps(dict(response.request.headers), indent=2))
    print("\nRequest Headers:")
    for key, value in response.request.headers.items():
        print(f"{key}: {value}")

    print(f"\nResponse:")
    print(f"\nExpected: {expected_status}, Actual: {response.status_code}")
    print("\nResponse Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    print("\nResponse Body:\n", response.text)

    assert response.status_code == expected_status, (
        f"FAILED: Expected {expected_status}, got {response.status_code}"
    )
