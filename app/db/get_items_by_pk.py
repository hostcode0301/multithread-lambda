from db.dynamodb_resource import dynamodb_resource as _dynamodb_resource


def get_items_by_pk(pk: str) -> dict:
    response = _dynamodb_resource.query(
        KeyConditionExpression='PK = :pk',
        ExpressionAttributeValues={
            ':pk': pk
        }
    )
    return response
