from lib import hashing, textract
from io import BytesIO
from fastapi import APIRouter
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile
from lib import tools
from PIL import Image

router = APIRouter()

@router.post("/receipt/hash")
async def hash_receipt(api_key: str, receipt: Optional[dict]) -> str:
    if tools.validate_key(api_key):
        return hashing.hash_receipt(receipt) 
    return {"api_valid": False}


@router.post("/receipt/upload")
async def upload_receipt(file: UploadFile = File(...), enhance: Optional[bool] = False):
    receipt = await file.read()
    Image.open(BytesIO(receipt)).show()
    if output := textract.process_receipt(receipt, upscale=enhance):
        return output
    return {"detail": "Something went wrong"}    