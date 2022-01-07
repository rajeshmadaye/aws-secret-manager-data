#************************************************************************
## Lambda Function  : aws-secret-manager-data
## Description      : Lambda function to fetch secret manager data using API GW
## Author           :
## Copyright        : Copyright 2022
## Version          : 1.0.0
## Mmaintainer      :
## Email            :
## Status           : In Review
##************************************************************************
## Version Info:
## 1.0.0 : 25-Oct-2021 : Created first version to fetch SM data
##************************************************************************

import traceback
import boto3
import json
import base64
from botocore.exceptions import ClientError

# ***********************************************************************
# Class Definition
# ***********************************************************************
class SECRETREADER:
    # ************************************************************************
    # Class constructor
    # ************************************************************************
    def __init__(self, request):
        self.secret_name = request['secret_name']
        self.region_name = request['region_name']
        return

    # ************************************************************************
    # Function to run main logic for PDF processing request
    # ************************************************************************
    def run(self):
        secret = self.get_secret()
        res = {
            'statusCode' : 200,
            'result' : secret
            }
        response = self.prepare_proxy_response(res)
        return response
        

    def get_secret(self):   
        # Create a Secrets Manager client
        secret_value_response = {}
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=self.region_name
        )
    
        # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
        # We rethrow the exception by default.
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                raise e
            else:
                raise e
        else:
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                secret_value_response = json.loads(get_secret_value_response['SecretString'])
            else:
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])           
                
        return secret_value_response
            
    # ************************************************************************
    # Function to get defined proxy headers
    # ************************************************************************
    def get_proxy_headers(self):
        headers = {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials" : True
                }
        return headers

    # ************************************************************************
    # Function to prepare proxy response
    # ************************************************************************
    def prepare_proxy_response(self, res):
        response = {
            'statusCode' : res['statusCode'],
            'body' : self.prepare_response(res),
            'headers' :  self.get_proxy_headers(),
            'isBase64Encoded': False
            }
        return response
        

    # ************************************************************************
    # Function to prepare response 
    # ************************************************************************
    def prepare_response(self, res):
        response = { 'statusCode' : res['statusCode'], 'result' : res['result'] }
        resp = json.dumps(response)
        return resp

def get_empty_proxy_response():
    headers = {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials" : True
            }    
    response = {
        'statusCode' : 404,
        'body' : json.dumps({ 'result' : { 'errMessage' : 'Invalid Request'} }),
        'headers' :  headers,
        'isBase64Encoded': False
        }
    return response

def lambda_handler(event, context):
    rc = True
    response = get_empty_proxy_response()
    if 'resource' in event:
        resource        = event['resource'].split('/')[1]
        query_params    = event['queryStringParameters']
        if len(query_params) and 'secret_name' in query_params and 'region_name' in query_params:
            try:
                SR = SECRETREADER(query_params)
                response = SR.run()
                print("Lambda Execution Status :", rc)
            except Exception as inst:
                print("Error:: Unable to process request:", inst)
                traceback.print_exc()
    return response
