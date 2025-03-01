from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/tricky")
async def tricky(class_: str = Query(..., alias="class")):
    data = {
        "class": class_
    }
    return JSONResponse(content=data)
