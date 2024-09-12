""" File to house pillow utility functions """

import base64
from io import BytesIO


def create_base64_image(pillow_image):
    """
    Create base64 image from a pillow image
    """
    pillow_image = resize_image_if_too_large(pillow_image)
    return dump_pillow_to_base64_image_url_string(pillow_image)


def dump_pillow_to_base64_image_url_string(pillow, output_format='png'):
    """
    Provided a pillow Image get the base64_image_url_string from it.
    """
    buffer = BytesIO()
    pillow.save(buffer, format=output_format)
    mime_type = f'image/{output_format.lower()}'
    base64_data = base64.b64encode(buffer.getvalue()).decode()
    return f'data:{mime_type};base64,{base64_data}'


def resize_image_if_too_large(
        img,
        max_height_px=1000,
        max_width_px=1000):
    """
    Provided a base64 image url string it if needed
    """
    if img.width >= max_width_px:
        aspect_ratio = img.height / img.width
        new_height = int(max_width_px * aspect_ratio)
        img = img.resize((max_width_px, new_height))

    if img.height >= max_height_px:
        aspect_ratio = img.height / img.width
        new_width = int(max_height_px * aspect_ratio)
        img = img.resize((new_width, max_height_px))

    return img
