import uvicorn
from dependency_injector.wiring import inject, Provide
from typing import Optional
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from helpers import tools
from routers import receipt, image
app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "10.52.8.63:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image.router)
app.include_router(receipt.router)

app.on_event("startup")
async def startup_event():
    print("test")
    

@app.get("/")
async def read_root():
    return {"detail": "API's up and running."}


@app.get("/{api_key}")
async def read_call(api_key: str, effects: Optional[str] = None):
    if tools.validate_key(api_key):
        return {"api_valid": True, "effects": "blur"}
    return {"api_valid": False}    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)