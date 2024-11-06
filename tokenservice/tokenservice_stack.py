from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_iam as iam,
    Duration,
    CfnOutput,
    RemovalPolicy,
    AssetHashType
)
from constructs import Construct

class TokenserviceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket for website hosting
        website_bucket = s3.Bucket(
            self, "WebsiteBucket",
            website_index_document="index.html",
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=False,
                block_public_policy=False,
                ignore_public_acls=False,
                restrict_public_buckets=False
            ),
            public_read_access=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        # Deploy website with API URL replacement
        s3deploy.BucketDeployment(
            self, "DeployWebsite",
            sources=[s3deploy.Source.asset("./website")],
            destination_bucket=website_bucket
        )

        # Output the website URL
        CfnOutput(
            self, "WebsiteURL",
            value=website_bucket.bucket_website_url
        )

        # Create DynamoDB table
        token_table = dynamodb.Table(
            self, "TokenTable",
            table_name="TokenTable",
            partition_key={"name": "uuid", "type": dynamodb.AttributeType.STRING},
            time_to_live_attribute="expiry"
        )

        # Create Lambda functions
        issue_token_fn = _lambda.Function(
            self, "IssueTokenFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="issue_token.handler",
            code=_lambda.Code.from_asset("lambda_functions",
                bundling={
                    "command": [
                        "bash", "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                    ],
                    "image": _lambda.Runtime.PYTHON_3_9.bundling_image,
                    "user": "root"
                }
            )
        )

        validate_token_fn = _lambda.Function(
            self, "ValidateTokenFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="validate_token.handler",
            code=_lambda.Code.from_asset("lambda_functions",
                bundling={
                    "command": [
                        "bash", "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output"
                    ],
                    "image": _lambda.Runtime.PYTHON_3_9.bundling_image,
                    "user": "root"
                }
            )
        )

        # Grant DynamoDB permissions to Lambda functions
        token_table.grant_write_data(issue_token_fn)
        token_table.grant_read_write_data(validate_token_fn)

        # Create API Gateway
        api = apigw.RestApi(
            self, "TokenAPI",
            rest_api_name="Token Service API",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=['GET', 'POST', 'OPTIONS'],  # Specify the HTTP methods you need
                allow_headers=['*']
            )
        )

        # Create API resources and methods
        tokens = api.root.add_resource("tokens")

        # GET /tokens
        tokens.add_method(
            "GET",
            apigw.LambdaIntegration(
                issue_token_fn,
                proxy=True,
                integration_responses=[{
                    'statusCode': '200',
                    'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                }]
            ),
            method_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            }]
        )

        # POST /tokens
        tokens.add_method(
            "POST",
            apigw.LambdaIntegration(
                validate_token_fn,
                proxy=True,
                integration_responses=[{
                    'statusCode': '200',
                    'responseParameters': {
                        'method.response.header.Access-Control-Allow-Origin': "'*'"
                    }
                }]
            ),
            method_responses=[{
                'statusCode': '200',
                'responseParameters': {
                    'method.response.header.Access-Control-Allow-Origin': True
                }
            }]
        )
