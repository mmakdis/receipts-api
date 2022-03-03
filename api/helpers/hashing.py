"""The interface behind receipts hashing"""

import hashlib
import jellyfish
import json

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

