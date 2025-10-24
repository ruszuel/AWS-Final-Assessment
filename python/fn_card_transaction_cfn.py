import json
import boto3
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return json.JSONEncoder.default(self, o)

def handler(event, context):
    print(json.dumps(event['body']))
    card_no = json.loads(event['body'])['card_no']
    transactions = getTransacation(card_no)
    
    return {
        "statusCode": 200,
        "body": json.dumps(transactions, cls=DecimalEncoder)
    }

def getTransacation(card_no):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('card_accounts_transactions_cfn')
    response = table.get_item(
        Key={'card_no': card_no}
    )
    return response.get('Item', {}).get('transactions', [])
