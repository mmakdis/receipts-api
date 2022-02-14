import json
import config
import secrets

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