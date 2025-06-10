from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_logs as logs,
    aws_lambda_python_alpha as lambda_python,
    RemovalPolicy
)
from constructs import Construct

class ChatGptApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, branch_name: str, openai_api_key: str, execution_role_arn: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role.from_role_arn(
            self, "LambdaExecutionRole",
            role_arn=execution_role_arn
        )

        log_group = logs.LogGroup(self, "ChatGPTApiChatConversationLogGroup",
            log_group_name="/aws/lambda/ChatGPT-API-chat-conversation",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Lambda function itself
        fn = lambda_python.PythonFunction(
            self, f"ChatGptFunction",
            entry="lambda",
            index="lambda_function.py",
            handler="lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_13,
            role=role,
            function_name=f"ChatGPT-API-{branch_name}",
            log_group=log_group,
            environment={
                "OPENAI_API_KEY": openai_api_key
            }
        )

        # API Gateway REST API
        api = apigw.RestApi(
            self, "ChatGptApi",
            rest_api_name=f"chatgpt-api-{branch_name}"
        )

        # Generate API Key
        api_key = api.add_api_key(
            "ApiKey",
            api_key_name="chatgpt-api-key"
        )

        # Usage Plan including this key
        usage_plan = api.add_usage_plan(
            "UsagePlan",
            name="UsagePlan",
        )
        usage_plan.add_api_key(api_key)
        usage_plan.add_api_stage(stage=api.deployment_stage)

        # Add the resource path (same as branch_name)
        resource = api.root.add_resource(branch_name,
                                         default_cors_preflight_options=apigw.CorsOptions(
                                             allow_origins=apigw.Cors.ALL_ORIGINS,
                                             allow_methods=["POST", "OPTIONS"],
                                             allow_headers=["x-api-key", 'Content-Type'],
                                         )
                                        )

        # Attach method to Lambda, require API key
        resource.add_method(
            "POST",
            apigw.LambdaIntegration(fn),
            api_key_required=True,
            authorization_type=apigw.AuthorizationType.NONE,
            method_responses=[
                apigw.MethodResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Access-Control-Allow-Origin': True,
                    }
                )
            ]
        )