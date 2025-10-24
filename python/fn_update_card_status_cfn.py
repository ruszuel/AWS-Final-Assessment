import json
import boto3

def handler(event, context):
    request_body = json.loads(event['body'])
    response = update_card_status(request_body['card_no'], request_body['status'])

    return response

def update_card_status(card_no, status):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('card_accounts_transactions_cfn')

    if status.upper() not in ("ACTIVE", "INACTIVE"):
        return {
            'statusCode': 403,
            'body': f"Card Status must be ACTIVE or INACTIVE"
        }
    table.update_item(
        Key={
            'card_no': card_no
        },
        UpdateExpression="set #s = :s",
        ExpressionAttributeNames = {
            '#s': 'status'
        },
        ExpressionAttributeValues={
            ':s': status.upper()
        },
        ReturnValues="UPDATED_NEW"
    )
    return {
        'statusCode': 200,
        'body': f"Card Status changed to {status.upper()}"
    }