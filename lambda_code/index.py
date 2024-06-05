import json
import os
import boto3

table_name = os.environ['TABLE_NAME']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

def handler(event, context):
    try:
        for record in event['Records']:
            if record['eventName'] == 'ObjectCreated:Put':
                bucket = record['s3']['bucket']['name']
                key = record['s3']['object']['key']
                
                table.put_item(
                    Item={
                        'id': key,
                        'bucket': bucket,
                    }
                )

        return {
            'statusCode': 200,
            'body': json.dumps('File processed!')
        }
    except Exception as e:
        print(f"Error processing event: {e}")
        raise
