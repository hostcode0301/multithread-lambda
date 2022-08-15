from datetime import datetime
from db.dynamodb_resource import dynamodb_resource as _dynamodb_resource
import threading
import os


def update_item(pk: str, sk: str, new_text: str) -> dict:
    print((
        f"--> Process {os.getpid()} - Thread {threading.get_ident()}: "
        f"At {datetime.utcnow()} - Updating {pk}"
    ))

    response = _dynamodb_resource.update_item(
        Key={
            'PK': pk,
            'SK': sk
        },
        UpdateExpression='SET #text = :text',
        ExpressionAttributeNames={
            '#text': 'Text'
        },
        ExpressionAttributeValues={
            ':text': new_text
        },
        ConditionExpression='attribute_exists(PK) AND attribute_exists(SK)',
        ReturnValues='ALL_NEW'
    )
    return response
