import os
import csv
import json
import pytest
import requests
from utils.docx_generator.export_to_docx import append_test_results_to_docx

BASE_URL = "https://jsonplaceholder.typicode.com/posts"
TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "test_data_get.csv")
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
def test_get_post_by_id(data):
    tc_no = data["tc_no"].strip()
    tc_name = data.get("tc_name", f"TestCase_{tc_no}")
    post_id = data["postId"].strip()
    expected_status = int(data["expected_status_code"].strip())

    url = f"{BASE_URL}/{post_id}"
    headers = {
        "Accept": "application/json",
        "User-Agent": "pytest-automation-client"
    }

    response = requests.get(url, headers=headers)

    print(f"\n{'=' * 80}")
    print(f"Test Case: {tc_no} - {tc_name}")

    print("\nRequest:")
    print(f"\nURL: {url}")

    # ---- Request Headers ----
    print("\nRequest Headers:")
    for key, value in response.request.headers.items():
        print(f"{key}: {value}")

    print(f"{'=' * 80}")

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
            "URL": url,
            "Method": "GET",
            "Headers": dict(response.request.headers),
            # No 'Body' key for GET (export_to_docx treats missing Body as <none>)
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
