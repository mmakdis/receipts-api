"""The interface behind receipts data"""

import hashlib
import jellyfish
import json
import uuid
import sys
from . import tools
from dateutil import parser
from .image import textract

TRANSACTION = ["transactie", "transackie", "transaction"]
DATE = ["date", "datum", "receipt_date"]
AUTH = ["autorisatiecode", "autorisatie code", "authorizationcode", "authorization code"]
ID = ["receipt_id"]


def get_json(metadata: dict) -> bytes:
    """Dictionary to JSON

    Args:
        metadata (dict): a dictionary of metadata

    Returns:
        bytes: a JSON representation of the metadata encoded as bytes
    """
    return json.dumps(metadata, sort_keys=True).encode()


def get_dict(metadata: str) -> dict:
    """Reverse get_json()

    Args:
        metadata (str): the JSON dict representation

    Returns:
        dict: the pickle data.
    """
    return json.loads(metadata)


def hash_receipt(metadata: dict) -> str:
    """Hash a dictionary

    Args:
        metadata (dict): the returned metadata from /image/analyze

    Returns:
        str: SHA256 HEX
    """
    sha256 = hashlib.sha256()
    sha256.update(get_json(metadata))
    return sha256.hexdigest()


def receipts_similarity(receipt1: dict, receipt2: dict) -> float:
    """Compare two sets of dictionaries (Metadata)

    Args:
        receipt1 (dict): the first receipt dictionary (metadata)
        receipt2 (dict): _description_

    Returns:
        float: _description_
    """
    receipt1 = get_json(receipt1).decode("utf-8")
    receipt2 = get_json(receipt2).decode("utf-8")
    return jellyfish.jaro_similarity(receipt1, receipt2)


def receipts_difference(receipt1: dict, receipt2: dict) -> float:
    """Compare two sets of dictionaries and and see what's different
    Combine with receipts_similarity (>0.7 recommended).

    Args:
        receipt1 (dict): _description_
        receipt2 (dict): _description_

    Returns:
        float: _description_
    """
    shared_items = {k: receipt1[k] for k in receipt1 if k in
                    receipt2 and receipt1[k] == receipt2[k]}
    print(shared_items)

def unique_id() -> str:
    """Get a unique ID for a receipt.

    Returns:
        str: unique ID.
    """
    return str(uuid.uuid4())

def find_date(receipt_data: dict) -> str:
    pass

def get_heineken_products(receipt_data: dict) -> list:
    """Checks for Heineken products in a receipt.

    Args:
        receipt_data (dict): Receipt data dictionary

    Returns:
        list: list of heineken products data.
    """
    heineken = []
    for product in receipt_data["products"]:
        if "heineken" in product:
            heineken.append(product)
    return heineken

def get_standards(receipt_data: dict):
    """Check for standardized values in meta data and convert them to their
    representation.

    Args:
        receipt_data (dict): the processed receipt data.
    """
    standards = {}
    if "meta" not in receipt_data:
        return False
    meta = receipt_data["meta"]
    if transaction := tools.all_in(TRANSACTION, meta):
        try:
            standards["transaction"] = int(meta[transaction])
        except ValueError:
            ...
    if date := tools.all_in(DATE, meta):
        try:
            standards["date"] = parser.parse(meta[date])
        except Exception as e:
            print(f"{type(e).__name__}: {date}")
    if auth := tools.all_in(AUTH, meta):
        standards["auth"] = meta[auth]
    if _id := tools.all_in(ID, meta):
        try:
            standards["id"] = meta[_id]
        except ValueError:
            ...
    return standards
    
if __name__ == "__main__":
    img_bytes = tools.get_bytes(f"{sys.argv[1]}", format="jpeg")
    print({sys.argv[1]})
    response = textract.analyze_expense(img_bytes, upscale=False)
    #print(json.dumps(response, indent=4))
    print(get_standards(response))
