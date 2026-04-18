import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from src.llm_analyser import analyse_chunk
from src.patch_writer import generate_patches
from src.doc_patcher import apply_patches

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r") as f:
        return f.read()

@app.post("/heal/")
async def heal_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")[:1000]

    issues = analyse_chunk(text)
    patches, fixed_text = generate_patches(text, issues)

    os.makedirs("./data/raw_docs", exist_ok=True)
    file_path = f"./data/raw_docs/{file.filename}"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(fixed_text)

    apply_patches(
    file_path=file_path, 
    patches=patches, 
    original_text=text, 
    final_text=fixed_text
)

    return JSONResponse({
    "original": text,
    "fixed": fixed_text,
    "patches": patches, 
    "total": len(patches),

   
})

