import boto3
import os
import json
from media_manipulation import create_slide_show

BUCKET_NAME = os.getenv('BUCKET_NAME')
NOTIFICATIONS_QUEUE_URL = os.getenv('NOTIFICATIONS_QUEUE_URL')


def handle_create_animation(request):
    s3 = boto3.client('s3')
    request_id = request['request_id']
    photos = request['photos']

    def ensure_request_dir(request_id):
        os.system("mkdir -p /tmp/{}/source".format(request_id))
        os.system("mkdir -p /tmp/{}/video".format(request_id))

    def copy_object_to_dir(s3_input_key, destination):
        print("try to download {}".format(s3_input_key))
        os.system("mkdir -p /tmp/{}/source".format(request_id))
        with open(destination, 'wb+') as data:
            s3.download_fileobj(BUCKET_NAME, s3_input_key, data)

    def upload_object(source, key):
        with open(source, 'rb') as data:
            s3.upload_fileobj(data, BUCKET_NAME, key)

    def clear_workspace(request_id):
        os.system("rm -rf /tmp/{}".format(request_id))

    def notify(email, video_url):
        sqs = boto3.client('sqs')
        video_ready_request = {
            "video_url": video_url,
            "email": email
        }

        resp = sqs.send_message(
            QueueUrl=NOTIFICATIONS_QUEUE_URL,
            MessageBody=json.dumps(video_ready_request)
        )

    def get_download_url(key):
        url = s3.generate_presigned_url(
            'get_object',
            Params={
                "Bucket": BUCKET_NAME,
                "Key": key
            }
        )

        return url

    ensure_request_dir(request_id)
    for i, photo_key in zip(range(0, len(photos)), photos):
        source_filename = "/tmp/{}/source/photo_{}".format(request_id, i)
        copy_object_to_dir(photo_key, source_filename)

    create_slide_show(
        ["/tmp/{}/source/photo_{}".format(request_id, i) for i in range(0, len(photos))],
        "/tmp/{}/output.mp4".format(request_id)
    )

    video_dest_key = "animations/ready/{}/video.mp4".format(request_id)

    upload_object(
        "/tmp/{}/output.mp4".format(request_id),
        video_dest_key
    )

    notify(request['email'], get_download_url(video_dest_key))

    clear_workspace(request_id)