"""
This module offers helper methods that aren't really related to 1 topic 
and are used in more than 1 topic.
"""
import json
import config
import secrets
import io
from PIL import Image

def generate_key() -> str:
    generated_key = secrets.token_urlsafe(config.api_keys_size)
    return generated_key.replace("-", "_")


def validate_key(key: str) -> bool:
    """Returns True if the key is in the keys.json

    Args:
        key (str): the key to validate

    Returns:
        bool: True or False
    """
    with open("keys.json", "r") as keyfile:
        data = json.load(keyfile)
    if key in data:
        return True
    return False

def read_config():
    pass

def write_config():
    pass

def get_bytes(image: str, format='JPEG'):
    """
    Helper method to extract corresponding bytes if image would be saved as 'format'.
    :param image: The image.
    :param format: The format.
    """
    with Image.open(image) as img:
        buf = io.BytesIO()
        img.save(buf, format=format)
        return buf.getvalue()