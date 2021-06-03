import boto3
import os

SENDER = os.getenv('SENDER_EMAIL')


def notify(notification_request):
    if not 'email' in notification_request:
        raise Exception('invalid request, email is missing')

    if not 'video_url' in notification_request:
        raise Exception('invalid request, video url is missing')

    send_email(notification_request['email'], notification_request['video_url'])


TEXT_TEMPLATE = '''
Hello,

Here is your animation download URL: {}

Best
ACME
'''

HTML_TEMPLATE = '''
<html>
    <body>

    <p><strong>Hello,</strong></p>

    <p>
    Here is your animation download URL: <a href="{}">DOWNLOAD</a>
    </p>
    <p>
    Best<br/>
    ACME
    </p>
</body>
</html>
'''


def send_email(email, video_url):
    ses = boto3.client('ses')
    resp = ses.send_email(
        Source=SENDER,
        Destination={
            "ToAddresses": [
                email
            ]
        },
        Message={
            'Subject': {
                'Data': "Hurray, your animation is ready!!!",
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': TEXT_TEMPLATE.format(video_url),
                    'Charset': 'utf-8'
                },
                'Html': {
                    'Data': HTML_TEMPLATE.format(video_url),
                    'Charset': 'utf-8'
                },
            }
        }
    )

    print("Message sent with id: {}".format(resp['MessageId']))


if __name__ == '__main__':
    notify({
        "email": os.getenv('SENDER_EMAIL'),
        "video_url": "http://example/video.mp4"
    })