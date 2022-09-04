from . models import picture, great, result
from user.models import user

import boto3
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

from uuid import uuid4

def get_img_url(img):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    image = img
    image_type = "jpg"
    image_uuid = str(uuid4())
    s3_client.put_object(Body=image, Bucket='greatman-bucket', Key=image_uuid + "." + image_type)
    image_url = "http://image-bucket2.s3.ap-northeast-2.amazonaws.com/" + image_uuid + "." + image_type
    image_url = image_url.replace(" ", "/")
    return image_url

