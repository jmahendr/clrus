# Standard Library
import json
import logging
import os
import datetime

# External Library
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, os.environ['logLevel'], 40))


def lambda_handler(event, context):
    logger.info(f"Received {event=}")
    user_pool_id = os.environ['userPoolId']
    attributes_string = os.environ['attributes']
    email = event['email']

    attributes = attributes_string.split(',')
    filter = f"email=\'{email}\'"

    client = boto3.client("cognito-idp")
    response = client.list_users(
        UserPoolId=user_pool_id,
        AttributesToGet=attributes,
        Limit=1,
        Filter=filter
    )
    return json.dumps(response['Users'], default=datetime_handler)


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")
