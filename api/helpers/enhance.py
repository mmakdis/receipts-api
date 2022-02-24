# Image Enhancement using different methods
# i.e. Super Resolution. 

from numpy import block
import requests
import matplotlib.pyplot as plt
import sys
import cv2
from PIL import Image
from io import BytesIO
from skimage import data
from skimage.filters.thresholding import threshold_otsu, threshold_local

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
                'image': image,
            },
            headers={'api-key': api_key}
            )
        if "output_url" in r.json():
            a = BytesIO(requests.get(r.json()["output_url"]).content)
            Image.open(a).show()
            return requests.get(r.json()["output_url"]).content
        return None
    

class Algorithms():
    def __init__(self):
        pass
    
    def adaptive_threshold():
        image = data.page()
        
        global_thresh = threshold_otsu(image)
        binary_global = image > global_thresh
        block_size = 35
        binary_adaptive = threshold_local(image, block_size, offset=10)
        fig, axes = plt.subplots(nrows=3, figsize=(7, 8))
        ax0, ax1, ax2 = axes
        plt.gray()
        ax0.imshow(image)
        ax0.set_tilte("Image")
        ax1.imshow(binary_global)
        ax1.set_title("Global thresholding")
        ax2.imshow(binary_adaptive)
        ax2.set_title("Adaptive thresholding")
        for ax in axes:
            ax.axis("off")
        plt.show()
    
    def opencv_edsr(image):
        """Make use of the EDSR model (implemented in Tensorflow with OpenCV.

        Args:
            image (string): image path.
        """
        pass
    
if __name__ == "__main__":
    waifu2x = Waifu2x()
    waifu2x.deepai_api(open(sys.argv[1], 'rb'))