"""Replacement to Waifu2x's class focusing on DeepAPI methods and its wide API.
Only static methods, each method represents a wrapper around a DeeoAPI API method.

waifu2x -> https://deepai.org/machine-learning-model/waifu2x

zendo -> https://deepai.org/zendo
"""
import requests
from PIL import Image
from io import BytesIO
from PIL import Image

def waifu2x(image, api_key="344e8250-df49-42d9-9a73-84cc9c206596"):
    """Enhance an Image through DeepAI using Waifu2x.

    Args:
        image (str | bytes): if a string is provided, it is assumed as the path. Otherwise provide image's bytes.
        api_key (str, optional): the API key. Defaults to "344e8250-df49-42d9-9a73-84cc9c206596".
    """
    if isinstance(image, str):
        image = open(image, 'rb')
    r = requests.post(
        "https://api.deepai.org/api/waifu2x",
        files={
            'image': image,
        },
        headers={'api-key': api_key}
        )
    if "output_url" in r.json():
        a = BytesIO(requests.get(r.json()["output_url"]).content)
        Image.open(a).show()
        return requests.get(r.json()["output_url"]).content
    return None

def zendo(image, endpoint="prod", api_key="fb346ba9-8d8a-4f61-bd2d-593f702c5ae6"):
    """An AI agent for visual tasks.

    Args:
        image (str | bytes): if a string is provided, it is assumed as the path. Otherwise provide image's bytes.
        endpoint (str): the API endpoint, either production "prod" or development "dev". Defaults to "prod".
        api_key (str): the API key to Zendo.

    Returns:
        _type_: _description_
    """
    if endpoint not in ["dev", "prod"]:
        return None
    r = requests.post(
        "https://api.deepai.org/api/writingondocs-4178-dev",
        data={
            'image': 'YOUR_IMAGE_URL',
        },
        headers={'api-key': 'fb346ba9-8d8a-4f61-bd2d-593f702c5ae6'}
    )
    print(r.json())