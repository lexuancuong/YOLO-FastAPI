from fastapi import FastAPI, File, UploadFile, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import PIL.Image as Image
from base64 import b64decode, b64encode
from detection import run
import numpy as np
import io
import sys
app = FastAPI()

app.mount("/static", StaticFiles(directory="./static/"), name="static")
templates = Jinja2Templates(directory="templates")

class Item(BaseModel):
    image64: str
    number: int = Query(0)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/detect/")
async def create_upload_file(item: Item):
    #Get request and solve that request
    base64_data = item.image64.split(',')[1]
    plain_data = b64decode(base64_data)
    plain_data = np.array(Image.open(io.BytesIO(plain_data)))
    if item.number == 0: 
        name_path = run.inferenceYoLo(plain_data)
    else:
        name_path = run.inferenceVNFood(plain_data)
    return {'url': name_path}
