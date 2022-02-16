# Image Enhancement using different methods
# i.e. Super Resolution. 

import requests
from PIL import Image
from io import BytesIO
import sys

class Waifu2x():
    """waifu2x is an image scaling and noise reduction program for anime-style art and other types of photos.
    It's insanely good. It's open-source: https://github.com/nagadomi/waifu2x
    """

    def __init__(self):
        pass

    def deepai_api(self, image, api_key="344e8250-df49-42d9-9a73-84cc9c206596"):
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
                'image': open('../data/maximages/Data.jpg', 'rb'),
            },
            headers={'api-key': api_key}
            )
        if "output_url" in r.json():
            return requests.get(r.json()["output_url"]).content
        return None
