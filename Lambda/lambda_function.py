import json
import boto3
import uuid

# UPDATE YOUR AWS REGION HERE IF DIFFERENT
AWS_REGION = 'us-east-1'

# Initialize AWS clients
textract = boto3.client('textract', region_name=AWS_REGION)
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
sns = boto3.client('sns', region_name=AWS_REGION)

# UPDATE TABLE NAME TO YOUR DYNAMODB TABLE
TABLE_NAME = "Resumes"

# UPDATE SNS TOPIC ARN WITH YOUR OWN TOPIC ARN
TOPIC_ARN = "arn:aws:sns:us-east-1:<your-account-id>:ResumeUploadAlert"

# HELPER FUNCTION TO DETECT IF A LINE IS A SECTION HEADING
def is_section_heading(line):
    keywords = ["summary", "education", "skills", "projects", "experience", "certifications", "achievements", "profile"]
    return any(word in line.lower() for word in keywords) and len(line.strip()) < 40

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # EXTRACT BUCKET AND FILE NAME FROM S3 EVENT
    bucket = event['Records'][0]['s3']['bucket']['name']
    document = event['Records'][0]['s3']['object']['key']
    print(f"Processing file: {document} from bucket: {bucket}")

    # CALL AMAZON TEXTRACT TO EXTRACT TEXT FROM PDF
    response = textract.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}}
    )

    lines = [block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE']
    print("Textract extracted lines:")
    for line in lines:
        print(line)

    # INITIALIZE EMPTY FIELDS FOR STRUCTURED RESUME DATA
    parsed_resume = {
        'ResumeID': str(uuid.uuid4()),
        'SourceFile': document,
        'Name': '',
        'Email': '',
        'Phone': '',
        'Education': [],
        'Skills': [],
        'Projects': [],
        'Experience': [],
        'Certifications': []
    }

    # EXTRACT CONTACT INFORMATION (EMAIL, PHONE, NAME)
    for line in lines:
        if '@' in line and not parsed_resume['Email']:
            parsed_resume['Email'] = line.strip()
        if any(char.isdigit() for char in line) and len(line.strip()) >= 10 and not parsed_resume['Phone']:
            parsed_resume['Phone'] = line.strip()
        if not parsed_resume['Name'] and any(name_word in line.lower() for name_word in ['name', 'resume']) is False:
            parsed_resume['Name'] = line.strip()

    # EXTRACT CONTENT BY DETECTING SECTIONS (SKILLS, EDUCATION, ETC.)
    current_section = None
    for line in lines:
        if is_section_heading(line):
            current_section = line.lower()
            continue
        if current_section:
            if "education" in current_section:
                parsed_resume['Education'].append(line)
            elif "skill" in current_section:
                parsed_resume['Skills'].append(line)
            elif "project" in current_section:
                parsed_resume['Projects'].append(line)
            elif "experience" in current_section:
                parsed_resume['Experience'].append(line)
            elif "certificate" in current_section or "achievement" in current_section:
                parsed_resume['Certifications'].append(line)

    print("Parsed Resume Data:", parsed_resume)

    # SAVE STRUCTURED DATA TO DYNAMODB
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=parsed_resume)

    # SEND SNS NOTIFICATION ON SUCCESSFUL PARSING
    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="New Resume Parsed",
        Message=f"New resume processed: {parsed_resume.get('Name', 'Unknown')}"
    )

    return {
        'statusCode': 200,
        'body': json.dumps("Resume parsed and stored successfully!")
    }
