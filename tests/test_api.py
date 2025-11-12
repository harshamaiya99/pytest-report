import os
import csv
import json
import pytest
import requests
from utils.docx_generator.export_to_docx import append_test_results_to_docx

BASE_URL = "https://jsonplaceholder.typicode.com/posts"
TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "test_data.csv")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "..", "utils", "docx_generator", "template.docx")
TEST_RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def read_test_data():
    data_list = []
    with open(TEST_DATA_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_list.append(row)
    return data_list


@pytest.mark.parametrize("data", read_test_data())
def test_create_posts(data):
    tc_no = data["tc_no"].strip()
    tc_name = data.get("tc_name", f"TestCase_{tc_no}")
    user_id = data["userId"].strip()
    title = data["title"].strip()
    body = data["body"].strip()
    expected_status = int(data["post_status_code"].strip())

    payload = {"userId": int(user_id), "title": title, "body": body}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "pytest-automation-client"
    }

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

    try:
        assert response.status_code == expected_status
        assertion_result = f"PASSED: Expected {expected_status}, got {response.status_code}"
    except AssertionError as e:
        assertion_result = f"FAILED: {e}"
        raise

    finally:
        request_details = {
            "URL": BASE_URL,
            "Method": "POST",
            "Headers": dict(response.request.headers),
            "Body": payload
        }

        try:
            response_body = response.json()
        except ValueError:
            response_body = response.text

        response_details = {
            "Status Code": response.status_code,
            "Headers": dict(response.headers),
            "Body": response_body
        }

        append_test_results_to_docx(
            tc_no=tc_no,
            tc_name=tc_name,
            request_details=request_details,
            response_details=response_details,
            assertion_result=assertion_result,
            output_dir=TEST_RESULTS_DIR,
            template_path=TEMPLATE_PATH
        )
