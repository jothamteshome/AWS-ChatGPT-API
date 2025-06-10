import os
import json
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def lambda_handler(event, context):
    try:
        raw_body = event.get("body")
        if raw_body is None:
            return {
                "statusCode": 400,
                "headers": { "Content-Type": "application/json" },
                "body": json.dumps({ "error": "Missing request body", "event": event }),
            }

        body = json.loads(raw_body)
        messages = body.get("messages")
        if not messages:
            return {
                "statusCode": 400,
                "headers": { "Content-Type": "application/json" },
                "body": json.dumps({ "error": "Missing messages in body", "event": event }),
            }

        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=1
        )

        content = response.choices[0].message.content
        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({ "response": content })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({ "error": str(e) })
        }