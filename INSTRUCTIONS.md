# 🚀 Setup & Deployment Instructions

Welcome to the Serverless Resume Parser! Follow this interactive guide to get your project up and running on AWS. If you get stuck, check the tips along the way. Let's go! 🎉

---

## 🏁 Progress

⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ 0% | 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 100%

As you complete each step, check the boxes below to track your progress!

---

## 🗂️ Quick Links
- [Prerequisites](#-prerequisites-checklist)
- [1. Create IAM Role](#1-create-iam-role-for-lambda)
- [2. Create S3 Bucket](#2-create-s3-bucket)
- [3. Create DynamoDB Table](#3-create-dynamodb-table)
- [4. Set Up SNS Topic](#4-set-up-sns-topic-for-email-alerts)
- [5. Create Lambda Function](#5-create-lambda-function)
- [6. Add Lambda Code](#6-add-lambda-code)
- [7. Add S3 Trigger](#7-add-s3-trigger-to-lambda)
- [8. Test the Full Flow](#8-test-the-full-flow)
- [Common Pitfalls & Pro Tips](#-common-pitfalls--pro-tips)

---

## ✅ Prerequisites Checklist
- [ ] **AWS Account** (not root user)
- [ ] **Region:** us-east-1 (N. Virginia)
- [ ] **AWS CLI** installed ([Install Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- [ ] **Sample resume PDF** ready to upload

---

### 1️⃣ Create IAM Role for Lambda

- [ ] Go to **IAM > Roles > Create role** ([AWS IAM Docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create.html))
- [ ] Choose **Lambda** as the trusted entity
- [ ] Click **Next**
- [ ] Attach these policies:
  - [ ] `AmazonTextractFullAccess`
  - [ ] `AmazonDynamoDBFullAccess`
  - [ ] `AmazonS3ReadOnlyAccess`
  - [ ] `CloudWatchLogsFullAccess`
  - [ ] `AmazonSNSFullAccess`
- [ ] Name your role: `ResumeParserLambdaRole`
- [ ] Click **Create role**

> 💡 **Tip:** This role gives Lambda all the permissions it needs to work with AWS services!

---

### 2️⃣ Create S3 Bucket

- [ ] Go to **S3 > Create bucket** ([AWS S3 Docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html))
- [ ] Name it: `resume-parser-bucket-123`
- [ ] Set region to **us-east-1**
- [ ] (Optional) Adjust public access settings as needed
- [ ] Click **Create bucket**

> 📦 **Pro Tip:** Use a unique bucket name to avoid conflicts with existing buckets in AWS.

---

### 3️⃣ Create DynamoDB Table

- [ ] Go to **DynamoDB > Create Table** ([AWS DynamoDB Docs](https://docs.aws.amazon.com/amazondynamodb/latest/gettingstartedguide/GettingStarted.CreateTable.html))
- [ ] Table name: `Resumes`
- [ ] Partition key: `ResumeID` (type: String)
- [ ] Click **Create table**

> 🗃️ **Note:** Double-check the table name and partition key—they must match what's in your Lambda code!

---

### 4️⃣ Set Up SNS Topic for Email Alerts

- [ ] Go to **SNS > Topics > Create topic** ([AWS SNS Docs](https://docs.aws.amazon.com/sns/latest/dg/sns-create-topic.html))
- [ ] Type: **Standard**
- [ ] Name: `ResumeUploadAlert`
- [ ] Click **Create topic**
- [ ] Click your new topic > **Create subscription**
- [ ] Protocol: **Email**
- [ ] Endpoint: *Your email address*
- [ ] Check your inbox and **confirm the subscription**

> 🔔 **You'll get an email every time a resume is processed!**

---

### 5️⃣ Create Lambda Function

- [ ] Go to **Lambda > Create function** ([AWS Lambda Docs](https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html))
- [ ] Name: `ResumeParserFunction`
- [ ] Runtime: **Python 3.12**
- [ ] Role: **Use existing role** → `ResumeParserLambdaRole`
- [ ] Click **Create function**

> 🐍 **Tip:** Make sure to select Python 3.12 for compatibility with the provided code.

---

### 6️⃣ Add Lambda Code

- [ ] Open your Lambda function in the AWS Console
- [ ] Replace the code with the contents of `Lambda/lambda_function.py` from this repo
- [ ] Update `TOPIC_ARN` in the code with your actual SNS topic ARN (see the SNS topic details page)

> ⚠️ **Don't forget:** Replace `<your-account-id>` in the ARN with your real AWS account ID!

---

### 7️⃣ Add S3 Trigger to Lambda

- [ ] In your Lambda function, go to **Configuration > Triggers**
- [ ] Click **Add trigger**
- [ ] Source: **S3**
- [ ] Bucket: `resume-parser-bucket-123`
- [ ] Event type: **PUT**
- [ ] Suffix: `.pdf`
- [ ] Click **Add**

> 🔗 **Tip:** This step connects your S3 bucket to Lambda so uploads trigger processing automatically.

---

### 8️⃣ Test the Full Flow!

- [ ] Go to **S3 > resume-parser-bucket-123**
- [ ] Click **Upload > Add Files** and select your resume PDF
- [ ] Wait 15–30 seconds ⏳
- [ ] Check:
  - [ ] **DynamoDB > Items**: See your new resume entry
  - [ ] **CloudWatch > Logs**: View Lambda logs
  - [ ] **Your email**: Look for the SNS alert

🎉 **All done! Your serverless resume parser is live!**

---

## 💡 Common Pitfalls & Pro Tips

- **IAM Permissions:** If Lambda can't access Textract, S3, or DynamoDB, double-check the attached policies.
- **Region Mismatch:** Make sure all your AWS resources are in the same region (`us-east-1`).
- **SNS Email Not Arriving:** Check your spam folder and confirm the subscription email.
- **DynamoDB Table Empty:** Double-check the table name and partition key in both the AWS Console and your Lambda code.
- **CloudWatch Logs Missing:** Attach `AWSLambdaBasicExecutionRole` or `CloudWatchLogsFullAccess` to your Lambda role.
- **PDF Not Triggering Lambda:** Make sure the S3 trigger is set up correctly and the file ends with `.pdf`.

---

*Need help? Check the [AWS docs](https://docs.aws.amazon.com/) or open an issue in this repo!* 