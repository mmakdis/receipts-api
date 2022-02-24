from kraken import binarization
from PIL import Image
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
from PIL import Image
from io import BytesIO
import cv2
import sys

def preprocess(image):
    # load the image
    image = cv2.imread(image)

    #resize image
    #image = cv2.resize(image,None,fx=0.7, fy=0.7, interpolation = cv2.INTER_CUBIC)

    #convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #calculate x & y gradient
    gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
    gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # blur the image
    blurred = cv2.blur(gradient, (3, 3))
    #return blurred

    # threshold the image
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
 
    thresh = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return thresh
    
def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    # uncomment above and comment below if you want to draw a polygon and not a rectangle
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                color=(0, 255, 0),
                thickness=5)
    return image

def decode_barcode(image):
    """Decode a barcode

    Args:
        image (BytesIO): the image STREAM. So this function wants the output of BytesIO(bytes)

    Returns:
        Decoded: The decoded data.
    """
    return decode(Image.open(image))

if __name__ == "__main__":
    #barcodes = glob(f"../data/maximages/{sys.argv[1]}")
    s = f"../data/maximages/{sys.argv[1]}"
    print(decode_barcode(s))
