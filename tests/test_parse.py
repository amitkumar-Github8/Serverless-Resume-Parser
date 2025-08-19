import json
import os
import sys

# Ensure Lambda module import works when running from repo root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Lambda.lambda_function import parse_resume_lines  # noqa: E402


def test_parse_minimal_contact():
    lines = [
        "Jane Doe",
        "Senior Data Scientist",
        "jane.doe@example.com | +1 (555) 123-4567",
    ]
    parsed = parse_resume_lines(lines)
    assert parsed['Name'] == "Jane Doe"
    assert parsed['Email'] == "jane.doe@example.com"
    assert "555" in parsed['Phone']


def test_parse_sections():
    lines = [
        "AMIT KUMAR",
        "Email: amitksamit@gmail.com",
        "Phone: 555-987-6543",
        "Skills",
        "Python, AWS, Lambda, DynamoDB",
        "Projects",
        "Serverless Resume Parser",
        "Experience",
        "Company ABC - Software Engineer",
        "Education",
        "BSc Computer Science - XYZ University",
        "Certifications",
        "AWS Certified Developer - Associate",
    ]
    parsed = parse_resume_lines(lines)
    assert parsed['Skills'] and any('Python' in l for l in parsed['Skills'])
    assert parsed['Projects'] and any('Resume' in l for l in parsed['Projects'])
    assert parsed['Experience'] and any('Company ABC' in l for l in parsed['Experience'])
    assert parsed['Education'] and any('University' in l for l in parsed['Education'])
    assert parsed['Certifications'] and any('AWS Certified' in l for l in parsed['Certifications'])
