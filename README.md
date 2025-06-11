# ChatGPT API with AWS CDK

A serverless REST API deployed with AWS CDK. It uses API Gateway and Lambda to wrap OpenAI’s GPT-4.1-mini chat API. Sends message history via POST and returns model responses. Includes API key protection and CORS support.

---

## Overview

This project provisions a simple, secure, and scalable REST API on AWS to interact with OpenAI's ChatGPT. It uses:

- **AWS CDK** for infrastructure-as-code deployment  
- **API Gateway** to expose a POST endpoint  
- **AWS Lambda** to handle chat completions  
- **OpenAI API (GPT-4.1-mini)** to generate responses  
- **API Key + CORS** for secure and flexible usage

The Lambda function receives a list of messages and returns the assistant's reply using OpenAI's chat API.

---

## Example Request

```http
POST /your-branch-name
Host: your-api-host.amazonaws.com
x-api-key: your-key
Content-Type: application/json
```

```json
{
  "messages": [
    { "role": "user", "content": "Hello!" }
  ]
}
```

---

## Response

```json
{
  "response": "Hi there! How can I help you today?"
}
```

---

## Setup & Deployment

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set environment variables:

```bash
export OPENAI_API_KEY=your-openai-key
export CHATGPT_API_EXECUTION_ROLE=your-lambda-role-arn
export CDK_DEFAULT_ACCOUNT=your-account-id
export CDK_DEFAULT_REGION=your-region
```

3. Deploy the stack:

```bash
cdk deploy --context branch_name=dev
```

---

## File Structure

- `app.py` – Entry point for the CDK app  
- `chat_gpt_api_stack.py` – Defines API Gateway + Lambda infrastructure  
- `requirements.txt` – CDK-level Python dependencies  
- `lambda/` – Source code for the Lambda function  
  - `lambda_function.py` – Lambda handler  
  - `requirements.txt` – Lambda-specific dependencies
