import json
import boto3
import os
import uuid
from slideshow_creation import handle_create_animation

def lambda_handler(event, context):
    
    print(event)
    if 'Records' in event:
        handle_create_animation(json.loads(event['Records'][0]['body']))

    return {
        'statusCode': 200,
        'body': {}
    }

   
