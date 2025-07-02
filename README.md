# Serverless-Resume-Parser

A scalable, serverless application that automates resume processing using AWS. Upload a PDF resume to Amazon S3, and AWS Lambda (using Textract) extracts key details like name, skills, and education, storing them in DynamoDB. Notifications are sent via SNS, and all activity is logged in CloudWatch.

## Architecture
- **IAM**: Secure roles and permissions for Lambda
- **S3**: PDF upload triggers Lambda
- **Lambda**: Uses Textract for OCR, parses resume, stores data in DynamoDB, sends SNS notifications
- **DynamoDB**: Stores parsed resume data
- **CloudWatch**: Logs and monitors Lambda execution
- **SNS**: Email notifications on new resume uploads

## Lambda Function Logic
- Triggered by S3 upload
- Uses Textract to extract text from PDF
- Parses for name, skills, and education
- Stores parsed data in DynamoDB
- Sends SNS notification
- Logs all steps for monitoring

---

**Note:** Replace `<your-account-id>` in the Lambda code with your actual AWS account ID for SNS notifications.

---

## Issues Faced & How I Solved Them

### ✅ 1. Textract AccessDeniedException
**Error Message:**
```
User is not authorized to perform: textract:DetectDocumentText
```
**Cause:**
- The Lambda function's IAM role did not have permission to call textract:DetectDocumentText.

**Solution:**
- Attached the `AmazonTextractFullAccess` policy to the Lambda's execution role.
- Verified that the role was properly linked under the Lambda's "Configuration > Permissions" tab.

---

### ✅ 2. Textract InvalidS3ObjectException
**Error Message:**
```
Unable to get object metadata from S3. Check object key, region and/or access permissions.
```
**Cause:**
- The Lambda function (Textract) couldn't access the PDF in the S3 bucket due to:
  - Wrong region
  - Lack of permission
  - Bucket/object not publicly accessible

**Solution:**
- Ensured S3 bucket and Lambda were in the same region (`us-east-1`).
- Gave `s3:GetObject` permission to the Lambda role.
- Made sure the file was uploaded correctly and accessible in S3.

---

### ✅ 3. Lambda Timeout or Textract Endpoint Error
**Error Message:**
```
Textract failed: Could not connect to the endpoint URL
```
**Cause:**
- Lambda was deployed in a region where Textract is not available (e.g., `eu-north-1`).

**Solution:**
- Re-created the Lambda function in `us-east-1`, a region that supports Textract.
- Made sure all services (Lambda, S3, Textract, DynamoDB) were in the same region.

---

### ✅ 4. No Output in DynamoDB Table
**Symptoms:**
- Resume was uploaded to S3
- Logs printed resume data
- But no data was inserted into DynamoDB

**Cause:**
- DynamoDB `put_item()` was silently failing due to:
  - Wrong table name
  - Region mismatch
  - Missing primary key (`ResumeID`)

**Solution:**
- Ensured the table name in the Lambda matches the actual DynamoDB table.
- Verified that `ResumeID` is used as the partition key.
- Logged the resume data right before inserting into the table for debugging.

---

### ✅ 5. CloudWatch Logs Not Visible
**Symptoms:**
- Lambda triggered but no logs appeared in CloudWatch.

**Cause:**
- IAM role lacked permission to publish logs.

**Solution:**
- Attached `AWSLambdaBasicExecutionRole` or `CloudWatchLogsFullAccess` to the Lambda's IAM role.
- Added explicit `print()` and logging statements inside the Lambda function.

---

### ✅ 6. SNS Emails Not Delivered
**Cause:**
- SNS subscription was created but email confirmation was not accepted.

**Solution:**
- Opened email inbox and clicked the confirmation link in the SNS subscription request.
- Resent the confirmation if missed.
