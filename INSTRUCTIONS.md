# Setup & Deployment Instructions (Beginner-Friendly)

Welcome to the Serverless Resume Parser! This guide walks you through deploying the project on AWS.

---

## 1) Create an IAM User for AWS Console Access (optional for personal accounts)

- Create a user with programmatic and console access if you need a separate admin.
- Start with least-privilege policies where possible. For a quick demo, these managed policies are acceptable but should be tightened for production:
  - AmazonS3ReadOnlyAccess
  - AmazonDynamoDBFullAccess (prefer table-scoped policy in production)
  - AmazonTextractFullAccess
  - AWSLambda_FullAccess (prefer function-scoped custom policy later)
  - CloudWatchLogsFullAccess
  - AmazonSNSFullAccess (prefer topic-scoped policy later)
- Add an inline policy for iam:PassRole if you plan to create/update Lambda execution roles via this user.

Tip: This user will be your admin for deploying and managing the project.

---

## 2) Create an IAM Role for Lambda Execution

- IAM → Roles → Create Role
- Use Case: AWS Service → Lambda
- Name: ResumeLambdaExecutionRole
- Attach policies (or custom least-privilege equivalents):
  - AmazonS3ReadOnlyAccess
  - AmazonTextractFullAccess
  - AmazonDynamoDBFullAccess
  - CloudWatchLogsFullAccess
  - AmazonSNSFullAccess

Note: This role authorizes the Lambda to access S3, Textract, DynamoDB, CloudWatch, and SNS.

---

## 3) Create an S3 Bucket for Resumes

- S3 → Create bucket
- Bucket name: resume-parser-uploads-demo (choose a unique name)
- Region: Same as Lambda (e.g., us-east-1)
- Create bucket

---

## 4) Create a DynamoDB Table

- DynamoDB → Create Table
- Table name: ParsedResumes
- Partition key: ResumeID (String)
- Create table

---

## 5) Create an SNS Topic

- SNS → Create Topic
- Type: Standard
- Name: ResumeUploadAlerts
- Create topic, copy the Topic ARN
- Add your email subscription and confirm via email

---

## 6) Create the Lambda Function

- Lambda → Create Function
- Name: ResumeParserFunction
- Runtime: Python 3.12
- Execution Role: Use existing → ResumeLambdaExecutionRole
- Create Function

---

## 7) Add Code and Configure Environment Variables

- Replace the default code with Lambda/lambda_function.py from this repo
- Set environment variables (Configuration → Environment variables):
  - TABLE_NAME = ParsedResumes
  - TOPIC_ARN = arn:aws:sns:us-east-1:<your-account-id>:ResumeUploadAlerts
- Deploy the function

Note: The function uses Textract detect_document_text (synchronous). For very large documents, consider the asynchronous Textract APIs.

---

## 8) Add S3 Trigger to Lambda

- In the Lambda, Add trigger → S3
- Bucket: resume-parser-uploads-demo
- Event type: PUT
- Add

Tip: This connects S3 uploads to your Lambda automatically.

---

## 9) View Logs in CloudWatch

- CloudWatch → Logs → /aws/lambda/ResumeParserFunction
- Inspect recent invocations for debugging

---

## 10) Test the Flow

- Upload a PDF resume to the S3 bucket
- Lambda is triggered → Textract extracts text → data is parsed and saved to DynamoDB → SNS email is sent
- Logs appear in CloudWatch

---

## Optional: Least-Privilege Policy Examples

S3 (read the upload bucket only):

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::resume-parser-uploads-demo/*"
    }
  ]
}

DynamoDB (write to a single table):

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["dynamodb:PutItem"],
      "Resource": "arn:aws:dynamodb:us-east-1:<account-id>:table/ParsedResumes"
    }
  ]
}

SNS (publish to a single topic):

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["sns:Publish"],
      "Resource": "arn:aws:sns:us-east-1:<account-id>:ResumeUploadAlerts"
    }
  ]
}

---

Need help? Check AWS docs or open an issue in this repo.