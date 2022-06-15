import sys
import base64

from fastapi import FastAPI, Form
from PIL import Image
from io import BytesIO
sys.path.append("..")

# from .utils.utils import verifyUser
from lib.models.model import get_model
from lib.utils.config import Config

app = FastAPI(root_path="/api/v1", servers=[{"url": "/api/v1"}])

conf = Config("conf/conf.json")
model = get_model(conf)


@app.get("/")
async def root():
    return {"message": "Welcome to use Celery LaTex OCR!"}


@app.post("/latexocr")
async def predict(img: str = Form(...), user: str = Form(...), token: str = Form(...)):
    # print(img)
    # res = {"status": "-1", "data": ""}
    # if not verifyUser(user, token):
    #     res["status"] = "error"
    #     res["data"] = "Invalid user or token"
    #     return res
    image = Image.open(BytesIO(base64.b64decode(img)))
    # image.save('temp.png')
    pred = model(image)
    return pred


@app.get("/api/v1/latexocr/test")
async def test():
    imgpath = "../tmp/test-3.png"
    with open(imgpath, "rb") as f:
        imgstr = base64.b64encode(f.read())
    img = Image.open(BytesIO(base64.b64decode(imgstr)))
    r = model(img, out_list=False)
    print(r[0])
    return {"data": r}

