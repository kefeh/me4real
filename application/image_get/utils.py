from bson import ObjectId
from application.utils.utils import image_decode_save

def save_image(image, name):
    return image_decode_save(image, name, 'others')


def get_images():
    import os
    from m_dir import BASE_IMAGE_PATH

    new_path = os.path.join(BASE_IMAGE_PATH, 'others')
    if not os.path.exists(new_path):
        return []

    files_path = [os.path.abspath(x) for x in os.listdir(new_path)]
    
    return files_path