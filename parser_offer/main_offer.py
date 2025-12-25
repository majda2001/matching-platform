from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from offer_parser import parse_job_info 

app = FastAPI(title="Job Offer Parser")

class JobText(BaseModel):
    text: str

@app.post("/parse-job")
def parse_job(job: JobText):
    if not job.text:
        raise HTTPException(status_code=400, detail="Job text is empty")
    result = parse_job_info(job.text)
    if not result:
        raise HTTPException(status_code=500, detail="Parsing failed")
    return result

if __name__ == "__main__":
    uvicorn.run("main_offer:app", host="0.0.0.0", port=8002, reload=True)
