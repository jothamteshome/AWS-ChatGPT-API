import os
import aws_cdk as cdk
from chat_gpt_api_stack import ChatGptApiStack

app = cdk.App()

branch_name = app.node.try_get_context("branch_name")
openai_api_key = os.environ["OPENAI_API_KEY"]
execution_role_arn = os.environ["CHATGPT_API_EXECUTION_ROLE"]

ChatGptApiStack(app, f"chatgpt-api-{branch_name}",
               env=cdk.Environment(
                   account=os.environ["CDK_DEFAULT_ACCOUNT"], 
                   region=os.environ["CDK_DEFAULT_REGION"]
                   ),
                branch_name=branch_name,
                openai_api_key=openai_api_key,
                execution_role_arn=execution_role_arn

)

app.synth()