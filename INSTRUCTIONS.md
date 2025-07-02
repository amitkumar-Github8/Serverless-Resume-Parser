# 🚀 Setup & Deployment Instructions

Welcome to the Serverless Resume Parser! Follow this interactive guide to get your project up and running on AWS. If you get stuck, check the tips along the way. Let's go! 🎉

---

## ✅ Prerequisites Checklist
- [ ] **AWS Account** (not root user)
- [ ] **Region:** us-east-1 (N. Virginia)
- [ ] **AWS CLI** installed (optional, but handy)
- [ ] **Sample resume PDF** ready to upload

---

## 🛠 Step-by-Step Guide

### 1️⃣ Create IAM Role for Lambda
1. Go to **IAM > Roles > Create role**
2. Choose **Lambda** as the trusted entity
3. Click **Next**
4. Attach these policies:
   - `AmazonTextractFullAccess`
   - `AmazonDynamoDBFullAccess`
   - `AmazonS3ReadOnlyAccess`
   - `CloudWatchLogsFullAccess`
   - `AmazonSNSFullAccess`
5. Name your role: `ResumeParserLambdaRole`
6. Click **Create role**

💡 *Tip: This role gives Lambda all the permissions it needs to work with AWS services!*

---

### 2️⃣ Create S3 Bucket
1. Go to **S3 > Create bucket**
2. Name it: `resume-parser-bucket-123`
3. Set region to **us-east-1**
4. (Optional) Adjust public access settings as needed
5. Click **Create bucket**

---

### 3️⃣ Create DynamoDB Table
1. Go to **DynamoDB > Create Table**
2. Table name: `Resumes`
3. Partition key: `ResumeID` (type: String)
4. Click **Create table**

---

### 4️⃣ Set Up SNS Topic for Email Alerts
1. Go to **SNS > Topics > Create topic**
2. Type: **Standard**
3. Name: `ResumeUploadAlert`
4. Click **Create topic**
5. Click your new topic > **Create subscription**
6. Protocol: **Email**
7. Endpoint: *Your email address*
8. Check your inbox and **confirm the subscription**

🔔 *You'll get an email every time a resume is processed!*

---

### 5️⃣ Create Lambda Function
1. Go to **Lambda > Create function**
2. Name: `ResumeParserFunction`
3. Runtime: **Python 3.12**
4. Role: **Use existing role** → `ResumeParserLambdaRole`
5. Click **Create function**

---

### 6️⃣ Add Lambda Code
1. Open your Lambda function in the AWS Console
2. Replace the code with the contents of `Lambda/lambda_function.py` from this repo
3. Update `TOPIC_ARN` in the code with your actual SNS topic ARN (see the SNS topic details page)

⚠️ **Don't forget:** Replace `<your-account-id>` in the ARN with your real AWS account ID!

---

### 7️⃣ Add S3 Trigger to Lambda
1. In your Lambda function, go to **Configuration > Triggers**
2. Click **Add trigger**
3. Source: **S3**
4. Bucket: `resume-parser-bucket-123`
5. Event type: **PUT**
6. Suffix: `.pdf`
7. Click **Add**

---

### 8️⃣ Test the Full Flow!
1. Go to **S3 > resume-parser-bucket-123**
2. Click **Upload > Add Files** and select your resume PDF
3. Wait 15–30 seconds ⏳
4. Check:
   - [ ] **DynamoDB > Items**: See your new resume entry
   - [ ] **CloudWatch > Logs**: View Lambda logs
   - [ ] **Your email**: Look for the SNS alert

🎉 **All done! Your serverless resume parser is live!**

---

*Need help? Check the AWS docs or open an issue in this repo!* 