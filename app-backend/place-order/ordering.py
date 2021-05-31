import boto3
import json

def place_order(queue_url, order_request):
    sqs = boto3.resource('sqs')
    queue = sqs.Queue(queue_url)
    queue.send_message(
        MessageBody=json.dumps(order_request)
    )

