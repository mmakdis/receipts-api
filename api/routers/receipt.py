from helpers import hashing, textract, tools
from io import BytesIO
from fastapi import APIRouter
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from db import db

conn = db.DB()
conn.connect()

router = APIRouter()

@router.post("/receipt/test")
async def receipt_test(key: str) -> str:
    return {"ping": conn.ping()}

@router.post("/receipt/hash")
async def hash_receipt(api_key: str, receipt: Optional[dict]) -> str:
    if tools.validate_key(api_key):
        return hashing.hash_receipt(receipt) 
    return {"api_valid": False}


@router.post("/receipt/upload")
async def upload_receipt(file: UploadFile = File(...), enhance: Optional[bool] = False):
    if file.content_type not in ["image/png", "image/jpeg"]:
        return {"detail": "Invalid content type"}
    receipt = await file.read()
    # Image.open(BytesIO(receipt)).show()
    if output := textract.process_receipt(receipt, upscale=enhance):
        if "detail" in output:
            return output
        if dboutput := conn.add_receipt(output):
            return dboutput if dboutput["detail"] != "OK" else output
    return {"detail": "Something went wrong"}