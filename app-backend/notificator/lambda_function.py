import json

from notification import notify

def lambda_handler(event, context):
    for message in event['Records']:
        notify(json.loads(message['body']))