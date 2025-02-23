# Legal Document Summarizer

The **Legal Document Summarizer** is a Flask-based web application that uses **AWS Bedrock** and the **Titan Text G1 - Lite** model to summarize legal documents. It provides a structured JSON output with key details such as document type, key provisions, case background, court’s decision, legal implications, and a simplified summary.

---

## Features
- **AI-Powered Summarization**: Uses AWS Bedrock and the Titan Text G1 - Lite model to analyze and summarize legal documents.
- **Structured JSON Output**: Returns summaries in a well-structured JSON format.
- **Easy Integration**: Built with Flask for seamless integration with frontend applications.
- **Scalable Deployment**: Designed to be deployed on AWS Elastic Beanstalk for scalability and reliability.

---

## AWS Services Used
1. **AWS Bedrock**:
   - Used to access the **Titan Text G1 - Lite** model for AI-powered summarization.
   - Handles the prompt engineering and model invocation.

2. **AWS Elastic Beanstalk**:
   - Used to deploy and manage the Flask application.
   - Provides automatic scaling, load balancing, and monitoring.

3. **AWS IAM (Identity and Access Management)**:
   - Used to manage permissions for accessing AWS Bedrock and other AWS services.

4. **AWS EC2**:
   - Underlying compute service used by Elastic Beanstalk to host the Flask application.

5. **AWS S3 (Optional)**:
   - Can be used to store legal documents if the application is extended to handle file uploads.

---

## Prerequisites
Before deploying the application, ensure you have the following:

1. **AWS Account**:
   - Sign up for an AWS account if you don’t have one.

2. **AWS CLI**:
   - Install and configure the AWS CLI:
     ```bash
     aws configure
     ```

3. **Python 3.9+**:
   - Ensure Python 3.9 or later is installed.

4. **Dependencies**:
   - Install the required Python packages:
     ```bash
     pip install Flask boto3
     ```

---

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/legal-document-summarizer.git
cd legal-document-summarizer
```

### 1. Configure AWS Credentials

Ensure your AWS credentials are configured correctly:

```bash
aws configure
```

### 3. Set Up AWS Bedrock
Enable AWS Bedrock in your AWS account.

Ensure your IAM role has the necessary permissions to invoke the Bedrock model:
```bash
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "*"
        }
    ]
}
```

### 4. Deploy to AWS Elastic Beanstalk
Initialize Elastic Beanstalk:

```bash
eb init -p python-3.9 legal-summarizer
```

Create the Elastic Beanstalk Environment:

```bash
eb create legal-summarizer-env
```

Deploy the Application:
```bash
eb deploy
```
Access the Application:

Once deployed, Elastic Beanstalk will provide a URL for your application.
```bash
Example: http://legal-summarizer-env.eba-xxxxxxxx.us-east-1.elasticbeanstalk.com
```

##Running Locally

Install Dependencies:

```bash

pip install -r requirements.txt
```

Run the Flask Application:

```bash
python3 summarize.py
```
Access the Application:

Open your browser and navigate to http://127.0.0.1:5000/.


## Testing the Application
Send a POST Request:

Use curl or Postman to send a POST request to the /summarize endpoint:

```bash
curl -X POST http://127.0.0.1:5000/summarize \
-H "Content-Type: application/json" \
-d '{"document": "IN THE SUPREME COURT OF INDIA..."}'

```
Example Response:

```json

{
  "Document Type": "Court Judgment",
  "Key Provisions": "Interpretation of force majeure clause in commercial contracts.",
  "Case Background": "Dispute between XYZ Corporation and ABC Ltd. regarding breach of a commercial contract for the supply of industrial machinery.",
  "Court’s Decision": "The Supreme Court set aside the High Court's judgment and ruled in favor of the Appellant, holding the Respondent liable for breach of contract.",
  "Legal Implications": "This judgment serves as a precedent for interpreting force majeure clauses in commercial contracts, especially in cases involving pandemics.",
  "Simplified Summary": "The Supreme Court ruled that ABC Ltd. is liable for breaching a contract with XYZ Corporation due to delayed delivery of machinery. The Court clarified that the force majeure clause did not cover pandemic-related delays unless explicitly stated. ABC Ltd. was ordered to pay INR 10 crore in damages and bear litigation costs."
}
```
