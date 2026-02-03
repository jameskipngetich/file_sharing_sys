import requests
import boto3
from botocore.exceptions import ClientError
"""
Contains the api logic of the app

TO DO
    create login logic
    create uploading and downloading class/functions
"""

class Generate_presigned_url:
    def __init__(self, s3_client, client_methods, client_parameters, expires_in):
        self.client = s3_client    #enter client credentials, i.e s3 and region name
        self.methods = client_methods   #enter specific methods, i.e PUT for uploads and GET for downloads
        self.parameters = client_parameters    #enter method parameteres such as file_path, content type ...
        self.expires_in = expires_in    #url activity time

    def generate_url(self, client, method, parameters, expires_in):
        try:
            url = client.generate_presigned_url(
                ClientMethod=method,
                Params=parameters,
                ExpiresIn=expires_in
            )
        except ClientError:
                print(f"Error: Could not generate presigned url for method: {method}")
                raise
        return url

    def download_url(self, client, parameters, expires_in):
        client = boto3.client("s3")         # By default, this will use credentials from ~/.aws/credentials
        parameters = [] 
        expires_in = expires_in
        method = 'GET'
        url = self.generate_url(client=client,
        method=method,
        parameters=parameters,
        expires_in=expires_in
        )

        return url

    def upload_url(self, client, parameters, expires_in):
        client = boto3.client("s3")         # By default, this will use credentials from ~/.aws/credentials
        parameters = [] 
        expires_in = expires_in
        method = 'PUT'
        url = self.generate_url(client=client,
        method=method,
        parameters=parameters,
        expires_in=expires_in
        )

        return url

