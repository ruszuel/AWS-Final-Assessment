import json
import boto3
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return json.JSONEncoder.default(self, o)


def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('card_accounts_transactions_cfn')
    response = table.scan()['Items']
    
    return {
        "statusCode": 200,
        "body": json.dumps(response, cls=DecimalEncoder, indent=2)
    }