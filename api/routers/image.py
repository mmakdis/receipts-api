from fastapi import APIRouter
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile
from helpers import tools

router = APIRouter()

@router.post("/image/analyze")
async def analyze_image(api_key: str, image: UploadFile = File(...)):
    if tools.validate_key(api_key):
        return {"api_valid": True}
    return {"api_valid": False}

@router.post("/image/enhance")
async def enhance_image(api_key: str, image: UploadFile = File(...)):
    if tools.validate_key(api_key):
        ...
    return {"api_valid": False}
