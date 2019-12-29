from bson import ObjectId
from application.utils.utils import image_decode_save, list_files, BASE_URl, delete_image_from_bucket

def save_image(image, name):
    return image_decode_save(image, name, 'others')


def get_images():
    # import os
    # from m_dir import BASE_IMAGE_PATH

    # new_path = os.path.join(BASE_IMAGE_PATH, 'others')
    # if not os.path.exists(new_path):
    #     return []

    # files_path = [os.path.abspath(x) for x in os.listdir(new_path)]
    bucket = 'me4real-storage'
    all_images = list_files(bucket)
    file_urls = [f"{BASE_URl}/{object_value['key']}" for object_value in all_images]

    return file_urls


def delete_image(image_url):
    image_key = image_url.split('/')[-1]

    delete_image_from_bucket(image_key)

    return True