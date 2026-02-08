import boto3
import uuid
import json
from datetime import datetime
from botocore.exceptions import ClientError

"""
This python program, contains the code for the lambda handler
It has logic on generating presigned s3 urls for uploading and downloading files from our repo
"""
# Initialize clients
s3_client = boto3.client('s3')
dynamo_db = boto3.resource('dynamodb')
table = dynamo_db.Table('secure-fle-db')        # TODO: create a dynamodb table named so
BUCKET_NAME = "mybucket"                        # TODO: enter the name of the s3 bucket to be used
PRESIGNED_URL_EXPIRY = "300"                    # 5 minutes


def lambda_handler(event, context):
    """
    Generate presigned url and
    save file metadata in dynamodb table
    """

    try:
        # Extract filename and content-type
        body = json.loads(event['body'])
        filename = body['filename']
        content_type = body['content-type']

        # Get the user_id
        user_id = body.requestContext.authorizer.claims['sub']

        # Generate unique file_id and s3 key (user_id/file_id-filename)
        file_id = str(uuid.uuid4())
        s3_key = f'{user_id}/{file_id}-{filename}'

        # Generate pre-signed s3 url
        url = s3_client.generate_presigned_url(
            'put_object',
            {
                "Bucket": BUCKET_NAME,
                "key": s3_key,
                "content-type": content_type
            },
            PRESIGNED_URL_EXPIRY
        )

        # Save metadata to dynamodb
        dynamo_db.put_item(file_id=file_id)
        dynamo_db.put_item(user_id=user_id)
        dynamo_db.put_item(filename=filename)
        dynamo_db.put_item(s3_key=s3_key)
        dynamo_db.put_item(content_type=content_type)
        dynamo_db.put_item(upload_date=datetime.now())
        dynamo_db.put_item(status="PENDING")

        return{
            'statusCode': 200,
            'body': {
                'url': f'{url}',
                'file_id': f'{file_id}'
            }
        }


    except KeyError as e:
        return {
            'statusCode' : 400,
            'body' : json.dumps({'error': f"missing required field: {str(e)}"})
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body' : json.dumps({"error": "failed to generate upload URL"})
        }


