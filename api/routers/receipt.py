from matplotlib.pyplot import text
from helpers import receipt, tools
from helpers.image import textract
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
async def hash_receipt(api_key: str, receipt_data: Optional[dict]) -> str:
    if tools.validate_key(api_key):
        return receipt.hash_receipt(receipt_data) 
    return {"api_valid": False}


@router.post("/receipt/upload")
async def upload_receipt(file: UploadFile = File(...), enhance: Optional[bool] = False, antiFraud: Optional[bool] = False, noWriting: Optional[bool] = False):
    if file.content_type not in ["image/png", "image/jpeg"]:
        return {"detail": "Invalid content type"}
    receipt_data = await file.read()
    if output := textract.analyze_expense(receipt_data, upscale=enhance):
        if not receipt.get_heineken_products(output):
            return {"detail": "no heineken products found"}
        if "detail" in output:
            return output
        if dboutput := conn.add_receipt(output):
            return dboutput if dboutput["detail"] != "OK" else output
        return output
    return {"detail": "Something went wrong"}
