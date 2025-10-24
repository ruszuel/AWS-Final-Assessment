import json
import boto3

def handler(event, context):
    print("card-transaction process invoked")

    card_no = json.loads(event['body'])['card_no']
    transaction_type = json.loads(event['body'])['transaction_type']
    amount = json.loads(event['body'])['amount']
    trans_process = transaction_process(card_no, transaction_type, amount)

    return trans_process

def transaction_process(card_no, transaction_type, amount):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('card_accounts_transactions_cfn')
    tr_type = transaction_type.lower()

    if tr_type not in ('debit', 'credit'):
        return {
            "statusCode": 400,
            "body": f"Invalid transaction type: {tr_type}"
        }

    response = table.get_item(Key={'card_no': card_no})
    if 'Item' not in response:
        return {
            "statusCode": 404,
            "body": f"Card number {card_no} not found!"
        }
    
    item = response['Item']

    if tr_type == 'debit' and item['balance'] < amount:
        return {
            "statusCode": 400,
            "body": f"Insufficient funds"
        }
    
    if item['status'] != "ACTIVE":
        return {
            "statusCode": 403,
            "body": f"Card is inactive"
        }
    
    updated_balance = item['balance'] - amount if tr_type == 'debit' else item['balance'] + amount
    
    table.update_item(
        Key={'card_no': card_no},
        UpdateExpression="SET transactions = list_append(if_not_exists(transactions, :empty_list), :new_transaction), balance = :new_balance",
        ExpressionAttributeValues={
            ':new_transaction': [{'transaction_type': tr_type, 'amount': amount}],
            ':empty_list': [],
            ':new_balance': updated_balance
        }
    )

    item['balance'] = updated_balance

    return {
        "statusCode": 200,
        "body": f"Transaction successful. New balance: {updated_balance}"
    }
