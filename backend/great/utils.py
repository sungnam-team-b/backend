from . models import picture, great, result
from user.models import user
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import boto3
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from backend.settings import AWS_BUCKET_REGION, AWS_STORAGE_BUCKET_NAME

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
    '''
    s3 bucket에 연결하는 함수 
    '''
    s3 = boto.client('s3',region_name = AWS_BUCKET_REGION, aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
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

def s3_get_image_url(s3, filename : str):
    '''
    image url을 불러오는 함수 
    '''
    return f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_BUCKET_REGION}.amazonaws.com/{filename}'

def get_ai_result(image):
    list1 = []
    list2 = []
    rank = []
    k=0
    model = load_model('./model/keras_model.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open('./picture/test1.jpg')
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    print(prediction)
    for i in range(0,len(prediction[0])):
        list1.append(prediction[0,i])
        list2.append(prediction[0,i])
    list2.sort(reverse=True)
    list2 = list2[0:3]
    for j in range(0,3):
        for i in range(1,len(prediction[0])):
            if(list1[i]==list2[j+1]):
                rank.append(i)
    # for i in range(1,len(prediction[0])):
    #     if(list1[i]==list2[0]):
    #         rank.append(i)
    # for i in range(1,len(prediction[0])):
    #     if(list1[i]==list2[1]):
    #         rank.append(i)
    # for i in range(1,len(prediction[0])):
    #     if(list1[i]==list2[2]):
    #         rank.append(i)
    great_dic = { name:value for name, value in zip(rank, list2) }
    return great_dic