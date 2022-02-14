import sys
import fastapi
import uvicorn
import tools
from typing import Optional, List
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import inspect
import textract
import barcode

# yes yes i will fix this later and have a proper setup.py
#sys.path.insert(1, os.path.join(sys.path[0], '..'))


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/api/{api_key}")
async def read_call(api_key: str, effects: Optional[str] = None):
    if tools.validate_key(api_key):
        return {"api_valid": True, "effects": "blur"}
    return {"api_valid": False}

@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

@app.post("/api/receipt/upload")
async def upload_receipt(file: UploadFile = File(...)):
    receipt = await file.read()
    output = textract.process_receipt(receipt)
    print(output)
    return output

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)