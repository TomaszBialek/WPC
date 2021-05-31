import json
import os
from ordering import place_order
from uuid import uuid4

def lambda_handler(request, context):
    # validation
    if not 'photos' in request:
        raise Exception('photos needs to be provided')

    if not 'email' in request:
        raise Exception('email is required')

    if len(request['photos']) <= 1:
        raise Exception('not enough photos selected')

    QUEUE_URL = os.getenv('QUEUE_URL')
    place_order(QUEUE_URL, {
        'email': request['email'],
        'photos': request['photos'],
        'request_id': str(uuid4())
    })

    return {
        'statusCode': 200,
        'body': "OK"
    }