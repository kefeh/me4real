import base64
import boto3


BASE_URl = "http://me4real-storage.s3.amazonaws.com"


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

    return response


def upload_file(file_name, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name.split('/')[-1]
    s3_client = boto3.client('s3')
    with open(file_name, "rb") as f:
        response = s3_client.upload_fileobj(f, bucket, object_name, ExtraArgs={'ContentType': "image/jpeg"})


    response = f'{BASE_URl}/{object_name}'

    return response


def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents