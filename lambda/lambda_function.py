import os
import json
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body"))
        messages = body["messages"]

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