from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import Dict, Any
import uvicorn
from cv_parser import extract_resume_text, parse_resume_with_gemini  

app = FastAPI(title="CV Parser")

@app.post("/parse-cv")
def parse_resume(file: UploadFile = File(...)):
    ext = file.filename.lower().split(".")[-1]
    if ext not in ["pdf", "docx", "txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(file.file.read())

    resume_text = extract_resume_text(temp_path)
    import os
    os.remove(temp_path)

    if not resume_text:
        raise HTTPException(status_code=500, detail="Text extraction failed")

    result = parse_resume_with_gemini(resume_text)
    if not result:
        raise HTTPException(status_code=500, detail="Parsing failed")

    return result

if __name__ == "__main__":
    uvicorn.run("main_cv:app", host="0.0.0.0", port=8001, reload=True)
