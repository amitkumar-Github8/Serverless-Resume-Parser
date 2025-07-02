# 🚀 Setup & Deployment Instructions

Welcome to the Serverless Resume Parser! Follow this interactive guide to get your project up and running on AWS. If you get stuck, check the tips along the way. Let's go! 🎉

---

## ✅ Prerequisites Checklist
- [ ] **AWS Account** (not root user)
- [ ] **Region:** us-east-1 (N. Virginia)
- [ ] **AWS CLI** installed ([Install Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
- [ ] **Sample resume PDF** ready to upload

---

<details>
<summary>### 1️⃣ Create IAM Role for Lambda</summary>

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

</details>

---

<details>
<summary>### 2️⃣ Create S3 Bucket</summary>

- [ ] Go to **S3 > Create bucket** ([AWS S3 Docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html))
- [ ] Name it: `resume-parser-bucket-123`
- [ ] Set region to **us-east-1**
- [ ] (Optional) Adjust public access settings as needed
- [ ] Click **Create bucket**

</details>

---

<details>
<summary>### 3️⃣ Create DynamoDB Table</summary>

- [ ] Go to **DynamoDB > Create Table** ([AWS DynamoDB Docs](https://docs.aws.amazon.com/amazondynamodb/latest/gettingstartedguide/GettingStarted.CreateTable.html))
- [ ] Table name: `Resumes`
- [ ] Partition key: `ResumeID` (type: String)
- [ ] Click **Create table**

</details>

---

<details>
<summary>### 4️⃣ Set Up SNS Topic for Email Alerts</summary>

- [ ] Go to **SNS > Topics > Create topic** ([AWS SNS Docs](https://docs.aws.amazon.com/sns/latest/dg/sns-create-topic.html))
- [ ] Type: **Standard**
- [ ] Name: `ResumeUploadAlert`
- [ ] Click **Create topic**
- [ ] Click your new topic > **Create subscription**
- [ ] Protocol: **Email**
- [ ] Endpoint: *Your email address*
- [ ] Check your inbox and **confirm the subscription**

> 🔔 **You'll get an email every time a resume is processed!**

</details>

---

<details>
<summary>### 5️⃣ Create Lambda Function</summary>

- [ ] Go to **Lambda > Create function** ([AWS Lambda Docs](https://docs.aws.amazon.com/lambda/latest/dg/getting-started-create-function.html))
- [ ] Name: `ResumeParserFunction`
- [ ] Runtime: **Python 3.12**
- [ ] Role: **Use existing role** → `ResumeParserLambdaRole`
- [ ] Click **Create function**

</details>

---

<details>
<summary>### 6️⃣ Add Lambda Code</summary>

- [ ] Open your Lambda function in the AWS Console
- [ ] Replace the code with the contents of `Lambda/lambda_function.py` from this repo
- [ ] Update `TOPIC_ARN` in the code with your actual SNS topic ARN (see the SNS topic details page)

> ⚠️ **Don't forget:** Replace `<your-account-id>` in the ARN with your real AWS account ID!

</details>

---

<details>
<summary>### 7️⃣ Add S3 Trigger to Lambda</summary>

- [ ] In your Lambda function, go to **Configuration > Triggers**
- [ ] Click **Add trigger**
- [ ] Source: **S3**
- [ ] Bucket: `resume-parser-bucket-123`
- [ ] Event type: **PUT**
- [ ] Suffix: `.pdf`
- [ ] Click **Add**

</details>

---

<details>
<summary>### 8️⃣ Test the Full Flow!</summary>

- [ ] Go to **S3 > resume-parser-bucket-123**
- [ ] Click **Upload > Add Files** and select your resume PDF
- [ ] Wait 15–30 seconds ⏳
- [ ] Check:
  - [ ] **DynamoDB > Items**: See your new resume entry
  - [ ] **CloudWatch > Logs**: View Lambda logs
  - [ ] **Your email**: Look for the SNS alert

🎉 **All done! Your serverless resume parser is live!**

</details>

---

*Need help? Check the [AWS docs](https://docs.aws.amazon.com/) or open an issue in this repo!* 