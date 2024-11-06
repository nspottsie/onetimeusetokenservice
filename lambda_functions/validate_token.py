import json
import jwt
import boto3
from datetime import datetime

SECRET_KEY = "your-secret-key"  # In production, use AWS Secrets Manager

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TokenTable')

def handler(event, context):
    try:
        # Get token from request body
        body = json.loads(event['body'])
        token = body.get('token')
        
        if not token:
            return {
                'statusCode': 401,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps({'message': 'Token not provided'})
            }
        
        # Decode JWT token
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return {
                'statusCode': 401,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps({'message': 'Token has expired'})
            }
        except jwt.InvalidTokenError:
            return {
                'statusCode': 401,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps({'message': 'Invalid token'})
            }
        
        # Check if UUID exists in DynamoDB
        response = table.get_item(
            Key={
                'uuid': payload['uuid']
            }
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 401,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps({'message': 'Token not found in database'})
            }
        
        # Delete the token from DynamoDB
        table.delete_item(
            Key={
                'uuid': payload['uuid']
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'message': 'Token validated successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        } 