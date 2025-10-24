import json
import boto3

def handler(event, context):
    print('api invoke')
    print(event)

    return register_card(json.loads(event['body']))

def register_card(item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('card_accounts_transactions_cfn')
    items = table.get_item(Key={'card_no': item['card_no']})
    if 'Item' in items:
        return {
            'statusCode': 400,
            'body': json.dumps('Card Already Registered')
        }
    
    item['status'] = 'INACTIVE'
    item['balance'] = 0
    item['transactions'] = []
    table.put_item(
        Item=item    
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Card Successfully Registered')
    }