from lambda_function import lambda_handler
import uuid

request = {
    "request_id": str(uuid.uuid4()),
    "email": "email",
    "photos": [
        "test_photo.jpg",
        "test_photo1.jpg",
        "test_photo3.jpg"
    ]
}
lambda_handler(request, {})