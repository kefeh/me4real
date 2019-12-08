import base64


def image_decode_save(image, image_name, category):
    """
        This function takes in an image and an id/category which it will use as an image name and
        then saves the image in the images folder and returns the appropriate path name for that
        image
    """

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

    return image_path