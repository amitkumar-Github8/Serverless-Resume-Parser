import json
import os
import re
import uuid
import logging
from urllib.parse import unquote_plus
from typing import List, Dict, Any

# Configure structured logging
logger = logging.getLogger()
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
logger.setLevel(logging.INFO)


# Environment-driven configuration (set in Lambda console)
TABLE_NAME = os.environ.get("TABLE_NAME", "")
TOPIC_ARN = os.environ.get("TOPIC_ARN", "")


def _get_boto_clients():
    """Create AWS clients/resources lazily and region-aware."""
    import boto3  # local import to avoid hard dependency during unit tests that import parsing only
    session = boto3.session.Session()
    region = os.environ.get('AWS_REGION') or session.region_name

    if region:
        textract = boto3.client('textract', region_name=region)
        dynamodb = boto3.resource('dynamodb', region_name=region)
        sns = boto3.client('sns', region_name=region)
    else:
        # Fallback to default config if region not resolved (useful in some local test scenarios)
        textract = boto3.client('textract')
        dynamodb = boto3.resource('dynamodb')
        sns = boto3.client('sns')
    return textract, dynamodb, sns


# Helper: detect if a line is a section heading
def is_section_heading(line: str) -> bool:
    keywords = [
        "summary",
        "education",
        "skills",
        "projects",
        "experience",
        "certifications",
        "achievements",
        "profile",
    ]
    text = line.strip().lower()
    return any(word in text for word in keywords) and 2 <= len(text) <= 40


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(\+?\d[\d\s().-]{8,}\d)")


def parse_resume_lines(lines: List[str]) -> Dict[str, Any]:
    """
    Pure parsing logic. Extracts fields from OCR lines.
    Returns a dict without ResumeID/SourceFile (added by handler).
    """
    parsed = {
        'Name': '',
        'Email': '',
        'Phone': '',
        'Education': [],
        'Skills': [],
        'Projects': [],
        'Experience': [],
        'Certifications': [],
    }

    # Email & phone
    for line in lines:
        if not parsed['Email']:
            m = EMAIL_RE.search(line)
            if m:
                parsed['Email'] = m.group(0)
        if not parsed['Phone']:
            m = PHONE_RE.search(line)
            if m:
                parsed['Phone'] = m.group(0)
        if parsed['Email'] and parsed['Phone']:
            break

    # Name heuristic: first non-empty line not containing email/phone keywords
    for line in lines:
        text = line.strip()
        if not text:
            continue
        if EMAIL_RE.search(text) or PHONE_RE.search(text):
            continue
        # Prefer lines with 2-4 capitalized words
        words = [w for w in re.split(r"\s+", text) if w]
        cap_words = [w for w in words if re.match(r"^[A-Z][a-zA-Z.'-]*$", w)]
        if 1 <= len(cap_words) <= 4:
            parsed['Name'] = text
            break
    if not parsed['Name'] and lines:
        parsed['Name'] = lines[0].strip()

    # Sections
    current_section = None
    for line in lines:
        if is_section_heading(line):
            current_section = line.lower()
            continue
        if not current_section:
            continue
        if "education" in current_section:
            parsed['Education'].append(line)
        elif "skill" in current_section:
            parsed['Skills'].append(line)
        elif "project" in current_section:
            parsed['Projects'].append(line)
        elif "experience" in current_section:
            parsed['Experience'].append(line)
        elif (
            "certificate" in current_section
            or "certification" in current_section
            or "certifications" in current_section
            or "achievement" in current_section
            or "achievements" in current_section
        ):
            parsed['Certifications'].append(line)

    return parsed


def lambda_handler(event, context):
    logger.info("event=%s", json.dumps(event))

    # Extract bucket and object from S3 event
    try:
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        document = record['s3']['object']['key']
    except (KeyError, IndexError) as e:
        logger.error("Invalid S3 event structure: %s", e)
        return {"statusCode": 400, "body": json.dumps("Bad event structure")}

    # URL-decode S3 object key (handles spaces, special chars)
    document = unquote_plus(document)
    logger.info("Processing file=%s bucket=%s", document, bucket)

    textract, dynamodb, sns = _get_boto_clients()

    # Textract OCR
    try:
        response = textract.detect_document_text(
            Document={'S3Object': {'Bucket': bucket, 'Name': document}}
        )
        lines = [b['Text'] for b in response.get('Blocks', []) if b.get('BlockType') == 'LINE']
    except Exception as e:
        logger.exception("Textract failed: %s", e)
        return {"statusCode": 500, "body": json.dumps("Textract error")}

    parsed_core = parse_resume_lines(lines)
    parsed_resume = {
        'ResumeID': str(uuid.uuid4()),
        'SourceFile': document,
        **parsed_core,
    }

    # Persist to DynamoDB if configured
    if not TABLE_NAME:
        logger.warning("TABLE_NAME env var not set; skipping DynamoDB write")
    else:
        try:
            table = dynamodb.Table(TABLE_NAME)
            table.put_item(Item=parsed_resume)
        except Exception as e:
            logger.exception("DynamoDB put_item failed: %s", e)
            return {"statusCode": 500, "body": json.dumps("Database error")}

    # Notify via SNS if configured
    if TOPIC_ARN:
        try:
            # Avoid sending PII: use source file reference instead of name/phone/email
            msg = f"New resume processed from file: {parsed_resume.get('SourceFile', 'unknown')}"
            sns.publish(TopicArn=TOPIC_ARN, Subject="New Resume Parsed", Message=msg)
        except Exception as e:
            logger.exception("SNS publish failed: %s", e)
            # Non-fatal: continue
    else:
        logger.info("TOPIC_ARN not set; skipping SNS notification")

    return {"statusCode": 200, "body": json.dumps("Resume parsed and stored successfully!")}
