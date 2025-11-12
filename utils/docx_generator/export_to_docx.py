import os
import json
from docx import Document

def append_test_results_to_docx(
        tc_no,
        tc_name,
        request_details,
        response_details,
        assertion_result,
        output_dir,
        template_path):

    """Append or create a .docx report for a test case using a template."""

    # Ensure results directory exists
    os.makedirs(output_dir, exist_ok=True)

    file_name = f"{tc_no} {tc_name}.docx"
    file_path = os.path.join(output_dir, file_name)

    # ---- Load template or existing doc ----
    if os.path.exists(file_path):
        doc = Document(file_path)
    else:
        if os.path.exists(template_path):
            doc = Document(template_path)
        else:
            doc = Document()
        doc.add_heading(f"{tc_no} - {tc_name}", level=1)
        doc.add_paragraph()

    # ---- Request Details ----
    doc.add_heading("Request Details:", level=2)

    # URL
    doc.add_paragraph("\nRequest URL:").runs[0].bold = True
    doc.add_paragraph(str(request_details.get("URL", "")), style="NoSpacing")

    # Method
    doc.add_paragraph("\nRequest Method:").runs[0].bold = True
    doc.add_paragraph(str(request_details.get("Method", "")), style="NoSpacing")

    # Headers
    doc.add_paragraph("\nRequest Headers:").runs[0].bold = True
    headers = request_details.get("Headers", {})
    for k, v in headers.items():
        doc.add_paragraph(f"{k}: {v}", style="NoSpacing")


    # Body
    doc.add_paragraph("\nRequest Body:").runs[0].bold = True
    # doc.add_paragraph(str(request_details.get("Body", "")), style="NoSpacing")
    doc.add_paragraph(json.dumps(request_details.get("Body", ""), indent=4), style="NoSpacing")

    # ---- Response Details ----
    doc.add_heading("Response Details:", level=2)

    # Status Code
    doc.add_paragraph("\nStatus Code:").runs[0].bold = True
    doc.add_paragraph(str(response_details.get("Status Code", "")), style="NoSpacing")

    # Headers
    doc.add_paragraph("\nResponse Headers:").runs[0].bold = True
    resp_headers = response_details.get("Headers", {})
    for k, v in resp_headers.items():
        doc.add_paragraph(f"{k}: {v}", style="NoSpacing")

    # Body
    doc.add_paragraph("\nResponse Body:").runs[0].bold = True
    # doc.add_paragraph(str(response_details.get("Body", "")), style="NoSpacing")
    doc.add_paragraph(json.dumps(response_details.get("Body", ""), indent=4), style="NoSpacing")

    # ---- Assertion Result ----
    doc.add_heading("Assertion Result", level=2)
    doc.add_paragraph(assertion_result, style="NoSpacing")

    # ---- Save ----
    doc.save(file_path)
