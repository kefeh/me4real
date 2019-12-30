import base64
import os
import boto3


S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
S3_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
S3_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY")
BASE_URl = 'http://{}.s3.amazonaws.com'.format(S3_BUCKET)# Connect to S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def image_decode_save(image, image_name, category):
    """
        This function takes in an image and an id/category which it will use as an image name and
        then saves the image in the images folder and returns the appropriate path name for that
        image
    """

    bucket = 'me4real-storage'

    image_info = image.split(';')[0].split(':')[-1]
    some_image = image.split(';')[1].split('base64,')[-1] + '=='
    image_ext = image_info.split('/')[-1]
    from m_dir import BASE_IMAGE_PATH
    import os

    category_path = os.path.join(BASE_IMAGE_PATH, category)
    f_image_name = image_name + '.' + image_ext
    image_path = os.path.join(category_path, f_image_name)
    # image_data = base64.b64decode(image)
    if not os.path.exists(BASE_IMAGE_PATH):
        os.makedirs(BASE_IMAGE_PATH)
    if not os.path.exists(category_path):
        os.makedirs(category_path)
    with open(image_path, 'wb') as image_file:
        image_file.write(base64.decodebytes(some_image.encode()))

    response = upload_file(image_path, bucket)
    # content = list_files(bucket)
    print(response)
    response = {'url': response} if response else {'error': "Could not save the image contact admin"}

    # Delete the temporal images folder and all its contents
    import shutil
    try:
        shutil.rmtree(BASE_IMAGE_PATH)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

    return response


def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name.split('/')[-1]
    with open(file_name, "rb") as f:
        response = s3_client.upload_fileobj(f, bucket, object_name, ExtraArgs={'ContentType': "image/jpeg"})

    response = f'{BASE_URl}/{object_name}'

    return response


def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    contents = []
    for item in s3_client.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents


def delete_image_from_bucket(file_name):
    """this function is used to delete the images in the bucket per filename"""
    s3_client.delete_object(Bucket=bucket, Key=file_name)