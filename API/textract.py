import boto3
import botocore
import sys
import json
from sympy import pretty_print
from tensorboard import summary
from textractprettyprinter.t_pretty_print_expense import get_string
from textractprettyprinter.t_pretty_print_expense import Textract_Expense_Pretty_Print, Pretty_Print_Table_Format
import io
import os
from PIL import Image, ImageDraw
import decimal
import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import cv2


bucket = "myreceiptsbuclet"

def draw_bounding_box(key, val, width, height, draw):
    # If a key is Geometry, draw the bounding box info in it
    if "Geometry" in key:
        # Draw bounding box information
        box = val["BoundingBox"]
        left = width * box['Left']
        top = height * box['Top']
        draw.rectangle([left, top, left + (width * box['Width']), top + (height * box['Height'])],
                       outline='black')

def print_labels_and_values(field):
    # Only if labels are detected and returned
    if "LabelDetection" in field:
        print(f"Label: {field['LabelDetection']['Text']}")
        # print(field.get("LabelDetection")["Geometry"])
    else:
        print("(no label)")

    if "ValueDetection" in field:
        # Confidence: field.get("ValueDetection")["Confidence"]
        print(f"Value: {field['ValueDetection']['Text']}")
        # print(field.get("ValueDetection")["Geometry"])
    else:
        print("(no value)")
        
        
def get_bytes(image: Image, format='JPEG'):
            """
            Helper method to extract corresponding bytes if image would be saved as 'format'.
            :param image: The image.
            :param format: The format.
            """
            buf = io.BytesIO()
            image.save(buf, format=format)
            return buf.getvalue()


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

def float_price(price: str) -> float:
    """Convert a string containing a price to a float. 
    If the string contains a comma, it'll be replaced with a period.

    Args:
        price (str): the item's price as a string.

    Returns:
        float: a cleaned price.
    """
    # sometimes the prices are for an example
    # 1,51 B
    # 3,95 A
    # 2,00 35%
    # to avoid these, split and take the first index word.
    price = price.strip()
    if not price or price.startswith("xx"):
        return
    price = price.split()[0]
    price = price.replace(',', ".")
    try:
        ## TODO: maybe switch to decimal.Decimal
        return float(price)
    except:
        raise ValueError("Not a valid price")
    
def clean_field(field) -> dict:
    """Clean the field's Geomtery keys
    (everything in it, boundingboxes, polygon etc)

    Args:
        field (dict): the expense or summary field.

    Returns:
        dict: the new cleaned dictionary.
    """
    if "LabelDetection" in field:
            field["LabelDetection"].pop("Geometry", None)
    if "ValueDetection" in field:
            field["ValueDetection"].pop("Geometry", None)
    return field

def parse_output(response):
    """Parses Textract's output and returns a structured JSON.

    Args:
        response (dict): the Textract's output (Analyze Expense)

    Returns:
        dict: a cleaned new output in JSON. 
    """    
    if "detail" in response:
        # print(response["detail"])
        return response
    pretty_printed_string = get_string(textract_json=response, output_type=[Textract_Expense_Pretty_Print.SUMMARY, Textract_Expense_Pretty_Print.LINEITEMGROUPS], table_format=Pretty_Print_Table_Format.fancy_grid)
    print(pretty_printed_string)
    quantity = ""
    metadata = {"vendor": "", "products": {}, "meta": {}, "total": {}}
    for expense_doc in response["ExpenseDocuments"]:
        for line_item_group in expense_doc["LineItemGroups"]:
            for line_items in line_item_group["LineItems"]:
                current_item = ""
                for expense_fields in line_items["LineItemExpenseFields"]:
                    #print_labels_and_values(expense_fields)
                    # all that bs making it harder to work with the data 
                    expense_fields = clean_field(expense_fields)
                    if expense_fields["Type"]["Text"] == "ITEM":
                        current_item = expense_fields["ValueDetection"]["Text"]
                        metadata["products"][current_item] = {}
                        if quantity:
                            metadata["products"][current_item]["quantity"] = quantity
                            quantity = ""
                    if expense_fields["Type"]["Text"] == "QUANTITY":
                        quantity = expense_fields["ValueDetection"]["Text"]
                    if expense_fields["Type"]["Text"] == "PRICE":
                        price = expense_fields["ValueDetection"]["Text"]
                        metadata["products"][current_item]["price"] = price
                    # reset current item
                    if expense_fields["Type"]["Text"] == "EXPENSE_ROW":
                        current_item = ""
        for summary_field in expense_doc["SummaryFields"]:
            summary_field = clean_field(summary_field)
            if summary_field["Type"]["Text"] == "VENDOR_NAME":
                metadata["vendor"] = summary_field["ValueDetection"]["Text"]
            if summary_field["Type"]["Text"] == "OTHER":
                metadata["meta"][summary_field["LabelDetection"]["Text"]] = summary_field["ValueDetection"]["Text"]
            if summary_field["Type"]["Text"] == "TOTAL":
                metadata["total"]["total"] = summary_field["ValueDetection"]["Text"]
            if summary_field["Type"]["Text"] == "SUBTOTAL":
                metadata["total"]["subtotal"] = summary_field["ValueDetection"]["Text"]
    return metadata

def process_receipt(image) -> dict:
    """Process a receipt with Textract API

    Args:
        image (bytes): the image in bytes.
    """
    s3_connection = boto3.resource('s3')
    client = boto3.client('textract', region_name="eu-west-2")
    response = client.analyze_expense(
        Document={'Bytes': image})

    if not response or not response["ExpenseDocuments"]:
        return {"detail": "No receipt found!"}
    for expense_doc in response["ExpenseDocuments"]:
        if not expense_doc["SummaryFields"]:
            return {"detail": "Not a valid receipt!"}
    return parse_output(response)

def process_text_detection(bucket, document):
    # Get the document from S3
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket, document)
    s3_response = s3_object.get()

    # # opening binary stream using an in-memory bytes buffer
    # stream = io.BytesIO(s3_response['Body'].read())

    # # loading stream into image
    # image = Image.open(stream)

    # Detect text in the document
    client = boto3.client('textract', region_name="eu-west-2")
    # client.ana
    # process using S3 object
    response = client.analyze_expense(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}})

    # Set width and height to display image and draw bounding boxes
    # Create drawing object
    # width, height = image.size
    # draw = ImageDraw.Draw(image)

def upload_bucket(image, bucket=bucket, overwrite=False) -> bool:
    """Upload an object as a bucket

    Args:
        image (str): the path of the image, not the object itself!
        bucket (str): the name of the bucket, defaults to the bucket variable.
        overwrite (bool, optional): Overwrite the object in the bucket if it exists. Defaults to False.
    """
    s3 = boto3.resource("s3")
    data = open(image, "rb")
    file_name = os.path.basename(data.name)
    try:
        s3.Object("myreceiptsbucket", file_name).load()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] != "404":
            raise

        # The object does not exist
        s3.Bucket('myreceiptsbucket').put_object(Key=file_name, Body=data)
        return True
    else:
        print(f"Object exists! Overwriting={overwrite}")
        # the object does exist
        if overwrite:
            s3.Bucket('myreceiptsbucket').put_object(Key=file_name, Body=data)
            return True
    return False

def main():
    # bucket = 'myreceiptsbucket'
    # document = 'UploadHIP15.jpeg'
    # process_text_detection(bucket, document)
    response = process_receipt(get_bytes(f"./data/maximages/{sys.argv[1]}", format="jpeg"))
    print(json.dumps(response, indent=4))
    

if __name__ == "__main__":
    main()