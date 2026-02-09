import boto3
import json
import re
from urllib.parse import unquote_plus
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Secure-upload-db')                  # make sure to update wih the created table name

def lambda_handler(event, context):
    """
    Triggered on s3 upload event
    extract file info 
    update upload status in dynamodb
    """

    try:
        # Extract s3_bucket and key from event
        bucket = event['Records'][0]['s3']['bucket']['name']
        s3_key = unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')         # Decode the key
        size = event['Records'][0]['s3']['object']['size']

        # parse file_id from key (user_id/file_id-filename)
        rest = s3_key.split("/", 1)
        file = rest.rsplit("-", 1)
        file_id = file[1]

        # Update dynamodb item
        table.update_item(
            Key={'file_id': file_id},
            UpdateExpression='SET #status = :status, #size = :size',
            ExpressionAttributeNames={
                '#status': 'status',
                '#size': 'size'
            },
            ExpressionAttributeValues={
                ':status': "COMPLETED",
                ':size': size
            }
        )

        print(f"Updated file {file_id} to COMPLETED status")

    except Exception as e:
        print(f'Error updating file metadata: {str(e)}')