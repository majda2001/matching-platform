from dotenv import load_dotenv
import google.generativeai as genai
import os
import sys
import json
import PyPDF2
import docx
import re
from datetime import datetime


load_dotenv()  # charge les variables depuis .env
API_KEY = os.getenv("API_KEY")
MODEL_NAME = "gemini-2.5-flash-lite"

if not API_KEY:
    print("Error: GOOGLE_API_KEY not set.", file=sys.stderr)
    sys.exit(1)

genai.configure(api_key=API_KEY)


def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}", file=sys.stderr)
        return None
    return text

def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {docx_path}: {e}", file=sys.stderr)
        return None
    return text

def extract_resume_text(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}", file=sys.stderr)
        return None

    ext = file_path.lower().split('.')[-1]
    if ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif ext == "docx":
        return extract_text_from_docx(file_path)
    elif ext == "txt":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()
    else:
        print(f"Error: Unsupported file format {file_path}", file=sys.stderr)
        return None


def calculate_years_of_experience(experiences):
    total_days = 0
    for exp in experiences:
        start = datetime.strptime(exp["startDate"], "%Y-%m-%d")
        end = exp.get("endDate")
        if end:
            end = datetime.strptime(end, "%Y-%m-%d")
        else:
            end = datetime.today()
        total_days += (end - start).days
    return round(total_days / 365, 2)


def parse_resume_with_gemini(resume_text):
    if not resume_text:
        return None

    prompt = f"""
Analyze the following resume text and extract information.
Output STRICTLY as JSON with these keys:
"name", "email", "phoneNumber", "profession", "experience",
"education", "skills", "languages", "certifications".

Instructions:
- All dates in yyyy-MM-dd format.
- Use null for missing fields, [] for empty lists.
- Correct typos if found.
- Extract name certifications from the CERTIFICATIONS section.
- Extract languages as objects with 'name' and 'level' (Courant, Intermédiaire, Débutant, or inconnu).
- Extract education as objects with 'degree' (Bac+3, Bac+5, Master, etc.) and 'field' (domain). 
  If only degree is mentioned, field="inconnu".
- Only include explicitly mentioned languages and educations.

--- RESUME TEXT START ---
{resume_text}
--- RESUME TEXT END ---
"""

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            parsed_data = json.loads(response_text[json_start:json_end])
        else:
            print("Error: No JSON found in Gemini response.", file=sys.stderr)
            parsed_data = {}

        
        languages = parsed_data.get("languages", [])
        new_languages = []
        for lang in languages:
            if isinstance(lang, str):
                new_languages.append({"name": lang.strip(), "level": "inconnu"})
            elif isinstance(lang, dict):
                name = lang.get("name", "").strip()
                level = lang.get("level", "inconnu").strip()
                if name:
                    new_languages.append({"name": name, "level": level})
        parsed_data["languages"] = new_languages

      
        educations = parsed_data.get("education", [])
        new_educations = []
        for edu in educations:
            if isinstance(edu, str):
                new_educations.append({"degree": edu.strip(), "field": "inconnu"})
            elif isinstance(edu, dict):
                degree = edu.get("degree", "").strip()
                field = edu.get("field", "inconnu").strip()
                if degree:
                    new_educations.append({"degree": degree, "field": field})
        parsed_data["education"] = new_educations

     
        keys = ["name", "email", "phoneNumber", "profession", "experience", "skills"]
        for key in keys:
            if key not in parsed_data:
                parsed_data[key] = None if key not in ["experience", "skills"] else []

      
        parsed_data["yearsOfExperience"] = calculate_years_of_experience(parsed_data.get("experience", []))

        return parsed_data

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error interacting with Gemini API: {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parse_resume.py <path_to_resume_file>", file=sys.stderr)
        sys.exit(1)

    resume_file_path = sys.argv[1]
    resume_text_content = extract_resume_text(resume_file_path)
    if not resume_text_content:
        print("Failed to extract text from resume. Exiting.", file=sys.stderr)
        sys.exit(1)

    print("=============== Resume content: ===============\n")
    print(resume_text_content)

    print("\n\n=============== Parsing resume with Gemini: ===============\n")
    parsed_info = parse_resume_with_gemini(resume_text_content)

    if parsed_info:
        print(json.dumps(parsed_info, indent=4, ensure_ascii=False))
    else:
        print("Failed to parse resume using Gemini.", file=sys.stderr)
        sys.exit(1)
