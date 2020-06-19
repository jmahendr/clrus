# Standard Library
import json
import logging
import os
import datetime

# External Library
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, os.environ['logLevel'], 40))

# Setup CORS
cors_domain = os.environ['CORS_DOMAIN']
cors = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': cors_domain
}

def lambda_handler(event, context):
    logger.info(f"Received {event=}")
    user_pool_id = os.environ['userPoolId']
    attributes_string = os.environ['attributes']
    email = event['queryStringParameters']['email']

    attributes = attributes_string.split(',')
    filter = f"email=\'{email}\'"

    client = boto3.client("cognito-idp")
    lis_user_resp = client.list_users(
        UserPoolId=user_pool_id,
        AttributesToGet=attributes,
        Limit=1,
        Filter=filter
    )
    response = {
        "statusCode": 200,
        "headers": cors,
        "body": json.dumps(lis_user_resp['Users'], default=datetime_handler)
    }
    return response


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")
