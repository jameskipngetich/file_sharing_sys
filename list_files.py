import boto3
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

"""
This python program contains logic used in the list files lambda handler
It reads file metadata from dynamodb and passes it on to the client
"""
dynamodb = boto3.resource('dynamodb')
table = dynamodb.table('secure-file')               # Replace with correct table name

def lambda_handler(event, context):
    """
    Read file metadata and pass on to client
    """
    try:
        # TODO Add logic here
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'body' : json.dumps({"error": "failed to generate upload URL"})
        }