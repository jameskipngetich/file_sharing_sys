import boto3
import json
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

"""
This python program contains logic used in the list files lambda handler
It reads file metadata from dynamodb and passes it on to the client
"""
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('secure-file')               # Replace with correct table name

def lambda_handler(event, context):
    """
    Read file metadata and pass on to authenticated client
    """
    try:

        user_id = event['requestContext']['authorizer']['claims']['sub']

        # Query dynamodb using GSI on user_id
        response = table.query(
            IndexName = 'user_id-index',
            KeyConditionExpression=Key('user_id').eq(user_id))

        # Get files from response
        files = response['Items']
            
        return {
                'statusCode': 200,
                'body': json.dumps({
                    'files':files,
                    'count': len(files)})
            }
        
    except ClientError as e :
        
        return {
            'statusCode': 500,
            'body': json.dumps({"error": "Failed to fetch uploaded files"})
        }    
    