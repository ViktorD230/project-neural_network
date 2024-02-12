import io
import uvicorn
import pathlib

from PIL import Image

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = pathlib.Path(__file__).parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get('/', response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/uploadfile/")
async def upload_photo(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    resized_image = image.resize((32, 32))
    output_buffer = io.BytesIO()
    resized_image.save(output_buffer, format="JPEG", quality=95)
    compressed_contents = output_buffer.getvalue()
    return StreamingResponse(io.BytesIO(compressed_contents), media_type="image/jpeg")


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
