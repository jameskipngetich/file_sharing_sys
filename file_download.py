import boto3
import json
from botocore.exceptions import ClientError

s3_client= boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Secure-file-db')        #  Remember to change name

BUCKET_NAME = 'my-bucket'                       # Remember to change name
PRESIGNED_URL_EXPIRY = 300

def lambda_handler(event, context):
    """
    Get file and user info from API Gateway response
    Confirm file ownership and permissions
    Generate s3 presigned url and send to client
    path: /files/{file_id}/download
    """

    try:

        # Extract file_id from path parameters
        file_id = event['pathParameters']['file_id']
        user_id = event['requestContext']['authorizer']['claims']['sub']

        # Get file metadata from dynamodb
        response = table.get_item(Key={'file_id':file_id})

        # Perform Authz
        if 'Item' not in response:
            return{
                'statusCode': 404,
                'body': json.dumps({"error": "File NOT FOUND"})
            }
        
        file_metadata = response['Item']
        if file_metadata['user_id'] != user_id:
            return{
                'statusCode': 403,
                'body': json.dumps({"error": "File NOT FOUND"})
            }
        
        s3_key = file_metadata['s3_key']
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": s3_key

            },
            ExpiresIn=PRESIGNED_URL_EXPIRY
        )
        return{
            'statusCode': 200,
            'body': json.dumps({
                'download_url': url,
                'file_id': file_id,
                'filename': file_metadata['filename']
            })
        }
      


    except KeyError as e:
        return {
            'statuscode': 400,
            'body': json.dumps({"error": f"Missing parameter {str(e)}"})
        }
    except ClientError as e:
        return{
            'statusCode': 500,
            'body': json.dumps({"error": "Failed to generate presigned url"})
        }
