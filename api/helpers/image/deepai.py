"""Replacement to Waifu2x's class focusing on DeepAPI methods and its wide API.
Only static methods, each method represents a wrapper around a DeeoAPI API method.

waifu2x -> https://deepai.org/machine-learning-model/waifu2x

zendo -> https://deepai.org/zendo
"""
from ast import Bytes
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from io import BytesIO
from PIL import Image
import sys

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
    if isinstance(image, str):
        image = open(image, 'rb')
    r = requests.post(
        "https://api.deepai.org/api/writingondocs-4178-dev",
        files={
            'image': image,
        },
        headers={'api-key': api_key}
    )
    return r.json()


def zendo_focus_receipt(image, output):
    ...

def zendo_draw_bounding_boxes(image, output) -> BytesIO:
    """Draw the boundingboxes of detected objects on a given image using 
    matplotlib and return a no-axis image.

    Args:
        image (BytesIO): the image in bytesIO.
        output (PIL.Image): the image in PIL.Image

    Returns:
        BytesIO: the image in PIL image.
    """
    img = Image.open(image)
    fig, ax = plt.subplots()
    plt.gcf().set_dpi(300)
    ax.imshow(img, interpolation='nearest')
    if "output" not in output:
        return None
    if "Objects" not in output["output"]:
        return None
    for bounding_box in output["output"]["Objects"]:
        co = bounding_box["bounding_box"]
        rect = patches.Rectangle((co[0], co[1]), co[2], co[3], linewidth=0.5,
                edgecolor='#22282D', facecolor='none', label="Label")
        plt.annotate(bounding_box["labels"]["label"], (co[0], co[1]), fontsize=3)
        ax.add_patch(rect)
    plt.set_cmap('hot')
    plt.axis('off') 
    buf = BytesIO()
    fig.savefig(buf, dpi=500, bbox_inches='tight')
    buf.seek(0)
    return Image.open(buf)

if __name__ == '__main__':
    a = sys.argv[1]
    img = open(a, 'rb')
    output = zendo(img)
    zendo_draw_bounding_boxes(img, output).show()