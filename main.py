from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "enhanced"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/enhance")
async def enhance_image(file: UploadFile = File(...)):
    filename = file.filename
    input_path = os.path.join(UPLOAD_DIR, filename)
    output_path = os.path.join(OUTPUT_DIR, filename)

    with open(input_path, "wb") as f:
        f.write(await file.read())

    subprocess.run([
        "realesrgan-ncnn-vulkan",
        "-i", input_path,
        "-o", output_path,
        "-n", "realesrgan-x4plus"
    ])

    with open(output_path, "rb") as out_file:
        return StreamingResponse(out_file, media_type="image/png")
