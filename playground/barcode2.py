import cv2
import sys

img = cv2.imread(f"../data/maximages/{sys.argv[1]}")
bardet = cv2.barcode_BarcodeDetector()
ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(img)
print(ok)