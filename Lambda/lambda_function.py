import json
import boto3
import uuid

textract = boto3.client('textract', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')

TABLE_NAME = "Resumes"
TOPIC_ARN = "arn:aws:sns:us-east-1:<your-account-id>:ResumeUploadAlert"

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    document = event['Records'][0]['s3']['object']['key']
    print(f"Processing file: {document} from bucket: {bucket}")

    response = textract.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}}
    )

    lines = [block['Text'] for block in response['Blocks'] if block['BlockType'] == 'LINE']
    print("Textract extracted lines:")
    for line in lines:
        print(line)

    # Simple parsing logic
    name = next((l for l in lines if "Amit" in l or "Name" in l), "Unknown")
    skills = [l for l in lines if any(skill in l.lower() for skill in ['python', 'aws', 'java', 'c++', 'docker'])]
    education = [l for l in lines if "university" in l.lower() or "bachelor" in l.lower()]

    parsed_data = {
        'ResumeID': str(uuid.uuid4()),
        'Name': name,
        'Skills': skills,
        'Education': education,
        'SourceFile': document
    }

    # Save to DynamoDB
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=parsed_data)

    # Send SNS notification
    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="New Resume Parsed",
        Message=f"New resume uploaded and parsed: {name}"
    )

    print("Parsed Resume Data:", parsed_data)
    return {
        'statusCode': 200,
        'body': json.dumps("Resume parsed and stored successfully!")
    }
