# API Test Automation

This project is an API test automation framework built using Python and Pytest. It tests the API endpoints of a sample JSON placeholder service and generates detailed reports in both HTML and DOCX formats.

## Project Structure

```
├── .gitignore
├── conftest.py
├── data
│   └── test_data.csv
├── reports
│   └── test_report.html
├── results
├── tests
│   └── test_api.py
└── utils
    └── docx_generator
        └── export_to_docx.py
```

## Requirements

- Python 3.x
- `pytest`
- `requests`
- `python-docx`

## Usage

1. Place your test data in `data/test_data.csv` following the specified format.
2. Run the tests using:
   ```sh
   pytest tests/test_api_post.py
   ```
    ```sh
   pytest -v --html=reports/test_report.html --self-contained-html
   ```

3. The test results will be saved in the `results` directory and a detailed HTML report will be generated in the `reports` directory.

## Customization

You can customize the title of the HTML report by modifying the `pytest_html_report_title` function in `conftest.py`.