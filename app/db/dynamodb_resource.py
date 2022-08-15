import boto3

dynamodb_resource = boto3.resource(
    'dynamodb',
    region_name='us-east-1'
).Table('multithread-lambda-dynamodb-table')
