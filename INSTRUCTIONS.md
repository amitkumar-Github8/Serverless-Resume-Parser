# Setup & Deployment Instructions (Beginner-Friendly)

Welcome to the Serverless Resume Parser! This guide will walk you through every step to get your project running on AWS, even if you're new to cloud services. Let's get started!

---

## 1. Create an IAM User for AWS Console Access

- [ ] Go to [IAM Console](https://console.aws.amazon.com/iam/)
- [ ] Click **Users** → **Add user**
- [ ] Name: `ResumeParserUser`
- [ ] Access type: Check **Programmatic access** and **AWS Management Console access**
- [ ] Set a password
- [ ] Permissions: Attach these AWS managed policies:
  - [ ] `AmazonS3FullAccess`
  - [ ] `AmazonDynamoDBFullAccess`
  - [ ] `AmazonTextractFullAccess`
  - [ ] `AWSLambda_FullAccess`
  - [ ] `CloudWatchFullAccess`
  - [ ] `AmazonSNSFullAccess`
- [ ] Add Inline Policy for `iam:PassRole`:
  - Name: `PassLambdaRolePolicy`
  - Policy JSON:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::<your-account-id>:role/ResumeLambdaExecutionRole"
    }
  ]
}
```

> Tip: This user will be your main admin for deploying and managing the resume parser project.

---

## 2. Create an IAM Role for Lambda Execution

- [ ] Go to **IAM → Roles → Create Role**
- [ ] Use Case: **AWS Service → Lambda**
- [ ] Name: `ResumeLambdaExecutionRole`
- [ ] Attach policies:
  - [ ] `AmazonS3ReadOnlyAccess`
  - [ ] `AmazonTextractFullAccess`
  - [ ] `AmazonDynamoDBFullAccess`
  - [ ] `CloudWatchLogsFullAccess`
  - [ ] `AmazonSNSFullAccess`
- [ ] Click **Create Role**

> Note: This role lets Lambda access all the AWS services it needs to process resumes.

---

## 3. Create an S3 Bucket for Resumes

- [ ] Go to **S3 → Create bucket**
- [ ] Bucket name: `resume-parser-uploads-demo`
- [ ] Region: Same as Lambda (e.g., `us-east-1`)
- [ ] (Optional) Disable Block Public Access only if necessary
- [ ] Click **Create bucket**

> Pro Tip: Use a unique bucket name to avoid conflicts with existing buckets in AWS.

---

## 4. Create a DynamoDB Table

- [ ] Go to **DynamoDB → Create Table**
- [ ] Table name: `ParsedResumes`
- [ ] Partition key: `ResumeID` (String)
- [ ] Leave other options as default
- [ ] Click **Create Table**

> Note: Double-check the table name and partition key—they must match what's in your Lambda code!

---

## 5. Create an SNS Topic

- [ ] Go to **SNS → Create Topic**
- [ ] Type: **Standard**
- [ ] Name: `ResumeUploadAlerts`
- [ ] Click **Create Topic**
- [ ] Copy the Topic ARN for Lambda use
- [ ] Add email subscription to the topic and confirm it in your email

> Tip: SNS will notify you by email every time a resume is processed!

---

## 6. Create Lambda Function

- [ ] Go to **Lambda → Create Function**
- [ ] Name: `ResumeParserFunction`
- [ ] Runtime: **Python 3.12**
- [ ] Execution Role: **Use existing role** → Select `ResumeLambdaExecutionRole`
- [ ] Click **Create Function**

> Tip: Make sure to select Python 3.12 for compatibility with the provided code.

---

## 7. Add Lambda Code

- [ ] Replace the default code with your updated resume parsing script (from this repo)
- [ ] Update these lines in your code:
  - `TABLE_NAME = "ParsedResumes"`
  - `TOPIC_ARN = "arn:aws:sns:us-east-1:<your-account-id>:ResumeUploadAlerts"`
- [ ] Click **Deploy**

> Note: This is where the magic happens! Your Lambda will now parse resumes and store the results.

---

## 8. Add S3 Trigger to Lambda

- [ ] In your Lambda, go to **Add trigger**
- [ ] Select **S3**
- [ ] Bucket: `resume-parser-uploads-demo`
- [ ] Event type: **PUT**
- [ ] Click **Add**

> Tip: This connects your S3 bucket to Lambda so uploads trigger processing automatically.

---

## 9. Enable CloudWatch Logs

- [ ] By default, Lambda logs to CloudWatch.
- [ ] To view logs:
  - Go to **CloudWatch → Logs**
  - Click on the log group: `/aws/lambda/ResumeParserFunction`
  - Inspect recent invocations and debug errors

> Tip: CloudWatch logs are your best friend for debugging and monitoring!

---

## How to Test It

- [ ] Upload a PDF resume to the S3 bucket
- [ ] It will trigger Lambda
- [ ] Text is extracted using Textract
- [ ] Structured data saved in DynamoDB
- [ ] Notification sent via SNS
- [ ] Logs appear in CloudWatch

> That's it! Your serverless resume parser is live and ready to use.

---

*Need help? Check the [AWS docs](https://docs.aws.amazon.com/) or open an issue in this repo!* 