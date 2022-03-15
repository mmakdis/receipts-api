"""Amazon Textract is a machine learning service that automatically extracts text, handwriting, and data from scanned documents.

This is a wrapper around the API.
"""
import boto3
import botocore
import io
import os
from io import BytesIO
from . import barcode, deepai
from PIL import Image

def upload_bucket(image, bucket = "myreceiptsbuclet", overwrite=False) -> bool:
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

def analyze_expense(img, upscale=False) -> dict:
    """Process a receipt with Textract API

    Args:
        image (bytes): the image in bytes.
    """
    if upscale:
        enhanced_image = deepai.waifu2x(img)
        img = enhanced_image or img
    image_stream = io.BytesIO(img)
    #Image.open(image_stream).show()

    client = boto3.client('textract', region_name="eu-west-2")
    response = client.analyze_expense(
        Document={'Bytes': img})

    if not response or not response["ExpenseDocuments"]:
        return {"detail": "No receipt found!"}
    for expense_doc in response["ExpenseDocuments"]:
        if not expense_doc["SummaryFields"]:
            return {"detail": "Not a valid receipt!"}
    try:
        output = _parse_analyze_expense_output(response)
    except KeyError as e:
        print(e)
        return {"detail": "Something went wrong, try enhancing the image maybe?"}
    output["barcode"] = {}
    barcode_data = barcode.decode_barcode(image_stream)
    if len(barcode_data) == 1:
        output["barcode"]["type"] = barcode_data[0][1]
        output["barcode"]["data"] = barcode_data[0][0].decode("utf-8")
    return output


def _float_price(price: str) -> float:
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


def _clean_field(field) -> dict:
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


def _draw_bounding_box(key, val, width, height, draw):
    # If a key is Geometry, draw the bounding box info in it
    if "Geometry" in key:
        # Draw bounding box information
        box = val["BoundingBox"]
        left = width * box['Left']
        top = height * box['Top']
        draw.rectangle([left, top, left + (width * box['Width']), top + (height * box['Height'])],
                    outline='black')


def _print_labels_and_values(field):
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


def _parse_analyze_expense_output(response):
    """Parses Textract's output and returns a structured JSON.

    Args:
        response (dict): the Textract's output (Analyze Expense)

    Returns:
        dict: a cleaned new output in JSON. 
    """    
    if "detail" in response:
        # print(response["detail"])
        return response
    quantity = ""
    metadata = {"vendor": "", "products": {}, "meta": {}, "total": {}}
    for expense_doc in response["ExpenseDocuments"]:
        for summary_field in expense_doc["SummaryFields"]:
            summary_field = _clean_field(summary_field)
            current_value = summary_field["ValueDetection"]["Text"].lower()
            current_type = summary_field["Type"]["Text"]
            if current_type == "VENDOR_NAME":
                metadata["vendor"] = current_value
            if current_type == "INVOICE_RECEIPT_DATE":
                metadata["meta"]["receipt_date"] = current_value
            if current_type == "INVOICE_RECEIPT_ID":
                metadata["meta"]["receipt_id"] = current_value
            if current_type == "OTHER":
                metakey = summary_field["LabelDetection"]["Text"].lower()
                metakey = metakey[:-1] if metakey.endswith(":") else metakey
                metadata["meta"][metakey] = current_value
            if current_type == "TOTAL":
                metadata["total"]["total"] = current_value
            if current_type == "SUBTOTAL":
                metadata["total"]["subtotal"] = current_value
        for line_item_group in expense_doc["LineItemGroups"]:
            for line_items in line_item_group["LineItems"]:
                current_item = ""
                for expense_fields in line_items["LineItemExpenseFields"]:
                    #print_labels_and_values(expense_fields)
                    # all that bs making it harder to work with the data 
                    expense_fields = _clean_field(expense_fields)
                    current_value = expense_fields["ValueDetection"]["Text"].lower()
                    if current_value == metadata["vendor"]:
                        continue
                    if expense_fields["Type"]["Text"] == "ITEM":
                        current_item = current_value
                        metadata["products"][current_item] = {}
                        if quantity:
                            metadata["products"][current_item]["quantity"] = quantity
                            quantity = ""
                    if expense_fields["Type"]["Text"] == "QUANTITY":
                        quantity = current_value
                    if expense_fields["Type"]["Text"] == "PRICE":
                        price = current_value
                        metadata["products"][current_item]["price"] = price
                    # reset current item
                    if expense_fields["Type"]["Text"] == "EXPENSE_ROW":
                        current_item = ""

    return metadata

