import json
import uuid
import time
import jwt
import boto3
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"  # In production, use AWS Secrets Manager
TTL_HOURS = 8

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TokenTable')

def handler(event, context):
    # Generate UUID
    token_uuid = str(uuid.uuid4())
    
    # Calculate expiry time
    expiry_time = int((datetime.now() + timedelta(hours=TTL_HOURS)).timestamp())
    
    # Create JWT token
    token_payload = {
        'uuid': token_uuid,
        'exp': expiry_time
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm='HS256')
    
    # Store in DynamoDB
    table.put_item(
        Item={
            'uuid': token_uuid,
            'expiry': expiry_time
        }
    )
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({
            'token': token
        })
    } 