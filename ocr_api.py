from fastapi import FastAPI
from pydantic import BaseModel
import pytesseract
from PIL import Image
import requests
from io import BytesIO

app = FastAPI()

# Tentukan path tesseract jika diperlukan
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Sesuaikan dengan path di komputermu

class ImageUrl(BaseModel):
    image_url: str

@app.post("/ocr/")
async def ocr_from_image(image_url: ImageUrl):
    try:
        # Ganti URL gambar dengan link unduhan langsung dari Google Drive
        drive_image_url = image_url.image_url.replace("view?usp=sharing", "uc?export=download")
        
        # Ambil gambar dari URL
        response = requests.get(drive_image_url)
        img = Image.open(BytesIO(response.content))
        
        # Ekstrak teks menggunakan Tesseract OCR
        text = pytesseract.image_to_string(img)
        
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}
