from . models import picture, great, result
from user.models import user
import boto3
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

from uuid import uuid4

# def get_img_url(img):
#     s3_client = boto3.client(
#         's3',
#         aws_access_key_id=AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=AWS_SECRET_ACCESS_KEY
#     )
#     image = img
#     image_type = "jpg"
#     image_uuid = str(uuid4())
#     s3_client.put_object(Body=image, Bucket='greatman-bucket', Key=image_uuid + "." + image_type)
#     image_url = "http://image-bucket2.s3.ap-northeast-2.amazonaws.com/" + image_uuid + "." + image_type
#     image_url = image_url.replace(" ", "/")
#     return image_url

def s3_connection():
    s3 = boto.client('s3',region_name = BUCKET_REGION, aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
    return s3

def s3_put_object(s3, bucket, filepath, filename):
    '''
    s3 bucket에 파일 업로드
    '''
    try:
        s3.upload_file(filepath, bucket, filename)
    except Exception as e:
        print(e)
        return False
    return True