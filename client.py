import imghdr
import requests
import readline
from timeit import default_timer as timer

url = "http://0.0.0.0:8000"

def send_image(image):
    files = {"file": image}
    return requests.post(url + "/api/receipt/upload", files=files)

if __name__ == "__main__":    
    while True:
        file_name = input("Image: data/maximages/")
        files = {"file": open(f"../data/maximages/{file_name}", "rb")}
        start = timer()
        response = requests.post(url + "/api/receipt/upload", files=files)
        end = timer()
        print(response.json())
        print(f"Took {(end - start):.2f}s to complete")
