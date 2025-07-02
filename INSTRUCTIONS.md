# 🚀 Setup & Deployment Instructions (Beginner-Friendly)

Welcome to the Serverless Resume Parser! This guide will walk you through every step to get your project running on AWS, even if you're new to cloud services. Let's get started! 🎉

---

<details>
<summary>1️⃣ <strong>Create an IAM User for AWS Console Access</strong></summary>

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

> 💡 **Tip:** This user will be your main admin for deploying and managing the resume parser project.

</details>

---

<details>
<summary>2️⃣ <strong>Create an IAM Role for Lambda Execution</strong></summary>

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

> 🛡️ **Note:** This role lets Lambda access all the AWS services it needs to process resumes.

</details>

---

<details>
<summary>3️⃣ <strong>Create an S3 Bucket for Resumes</strong></summary>

- [ ] Go to **S3 → Create bucket**
- [ ] Bucket name: `resume-parser-uploads-demo`
- [ ] Region: Same as Lambda (e.g., `us-east-1`)
- [ ] (Optional) Disable Block Public Access only if necessary
- [ ] Click **Create bucket**

> 📦 **Pro Tip:** Use a unique bucket name to avoid conflicts with existing buckets in AWS.

</details>

---

<details>
<summary>4️⃣ <strong>Create a DynamoDB Table</strong></summary>

- [ ] Go to **DynamoDB → Create Table**
- [ ] Table name: `ParsedResumes`
- [ ] Partition key: `ResumeID` (String)
- [ ] Leave other options as default
- [ ] Click **Create Table**

> 🗃️ **Note:** Double-check the table name and partition key—they must match what's in your Lambda code!

</details>

---

<details>
<summary>5️⃣ <strong>Create an SNS Topic</strong></summary>

- [ ] Go to **SNS → Create Topic**
- [ ] Type: **Standard**
- [ ] Name: `ResumeUploadAlerts`
- [ ] Click **Create Topic**
- [ ] Copy the Topic ARN for Lambda use
- [ ] Add email subscription to the topic and confirm it in your email

> 📢 **Tip:** SNS will notify you by email every time a resume is processed!

</details>

---

<details>
<summary>6️⃣ <strong>Create Lambda Function</strong></summary>

- [ ] Go to **Lambda → Create Function**
- [ ] Name: `ResumeParserFunction`
- [ ] Runtime: **Python 3.12**
- [ ] Execution Role: **Use existing role** → Select `ResumeLambdaExecutionRole`
- [ ] Click **Create Function**

> ⚙️ **Tip:** Make sure to select Python 3.12 for compatibility with the provided code.

</details>

---

<details>
<summary>7️⃣ <strong>Add Lambda Code</strong></summary>

- [ ] Replace the default code with your updated resume parsing script (from this repo)
- [ ] Update these lines in your code:
  - `TABLE_NAME = "ParsedResumes"`
  - `TOPIC_ARN = "arn:aws:sns:us-east-1:<your-account-id>:ResumeUploadAlerts"`
- [ ] Click **Deploy**

> 🧠 **Note:** This is where the magic happens! Your Lambda will now parse resumes and store the results.

</details>

---

<details>
<summary>8️⃣ <strong>Add S3 Trigger to Lambda</strong></summary>

- [ ] In your Lambda, go to **Add trigger**
- [ ] Select **S3**
- [ ] Bucket: `resume-parser-uploads-demo`
- [ ] Event type: **PUT**
- [ ] Click **Add**

> 🔁 **Tip:** This connects your S3 bucket to Lambda so uploads trigger processing automatically.

</details>

---

<details>
<summary>9️⃣ <strong>Enable CloudWatch Logs</strong></summary>

- [ ] By default, Lambda logs to CloudWatch.
- [ ] To view logs:
  - Go to **CloudWatch → Logs**
  - Click on the log group: `/aws/lambda/ResumeParserFunction`
  - Inspect recent invocations and debug errors

> 🔍 **Tip:** CloudWatch logs are your best friend for debugging and monitoring!

</details>

---

<details>
<summary>🧪 <strong>How to Test It</strong></summary>

- [ ] Upload a PDF resume to the S3 bucket
- [ ] It will trigger Lambda
- [ ] Text is extracted using Textract
- [ ] Structured data saved in DynamoDB
- [ ] Notification sent via SNS
- [ ] Logs appear in CloudWatch

🎉 **That's it! Your serverless resume parser is live and ready to use.**

</details>

---

*Need help? Check the [AWS docs](https://docs.aws.amazon.com/) or open an issue in this repo!* 