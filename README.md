# Amazon Lambda function to fetch secret manager detail using API Gateway.
This project contains source code and supporting files for a python based Amazon lambda function to fetch
secret manager contents for provided secret manager name and region name as a query parameter in API request.


Lambda function and API Gateway should be deployed to fetch secret manager detail.

## Pre-requsites
- Create new entry in using secret manager service.

## Features
- Lambda function and API GW environment can be deployed using SAM template.
- User can pass input record as a query parameters in API endpoint "secret" using "GET" method.
- If provided secret name is valid and exists in secret manager, then secret detail will be provided as an API response.


## Tech
Below are list of technologies used.
- [Python] - Python based lambda function.
- [boto3] - Python boto3 SDK used to interact with AWS services.

Below are list of AWS services used in this project.
- [SecretManager] - Boto3 client object used to interact with AWS secret manager service
- [Lambda]        - AWS Lambda function created.


## Package installation steps

User should use below command to create this package.
```bash
sam package --region $AWSRegion --profile $ProfileName --s3-bucket $BucketName --template-file $BuiltTemplate --output-template-file deploy.yaml
```

User should use below command to deploy this package.
```bash
sam deploy --region $AWSRegion --profile $ProfileName --s3-bucket $BucketName --template-file $BuiltTemplate --stack-name $StackName --capabilities CAPABILITY_IAM

```


## License
MIT

**Free Software, Keep Learning!**
