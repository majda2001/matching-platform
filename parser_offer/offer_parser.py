import google.generativeai as genai
import json


API_KEY = "AIzaSyDNcpRWQQWvTpyTF9ESrZRvyn9XXTp2VzM"
MODEL_NAME = "gemini-2.5-flash-lite"

genai.configure(api_key=API_KEY)


def parse_job_info(job_text):
    if not job_text:
        return None

    prompt = f"""
You are an information extraction system.

Extract ONLY the following fields from the job description.
Do NOT invent information.
If something is not mentioned, use null or [].

Return STRICTLY a JSON object with EXACTLY these keys:

- jobTitle: string or null
- companyName: string or null
- competences: list of key skills and technologies ONLY (short keywords)
- requiredExperienceYears: string or null (example: "0-1", "2+", "3-5")
- requiredLanguages: list of objects with "name" and "level" (e.g., {{"name": "English", "level": "Courant"}}). 
  If level is not specified, use "inconnu".
- certifications: list of certifications mentioned
- educations: list of objects with "degree" (Bac+3, Bac+5, Master, etc.) and "field" (domain of study). 
  If only degree is mentioned, set field to "inconnu".

Rules:
- competences must be concise keywords (e.g. "Python", "n8n", "LLMs", "SQL")
- Do NOT include tasks, soft skills, or long sentences
- Languages and educations must include level/field if mentioned

--- JOB DESCRIPTION START ---
{job_text}
--- JOB DESCRIPTION END ---
"""

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        text = response.text.strip()

        
        start = text.find("{")
        end = text.rfind("}") + 1
        if start == -1 or end == -1:
            print("JSON non trouvé dans la réponse Gemini")
            print(text)
            return None

        data = json.loads(text[start:end])

       
        schema = {
            "jobTitle": None,
            "companyName": None,
            "competences": [],
            "requiredExperienceYears": None,
            "requiredLanguages": [],
            "certifications": [],
            "educations": []
        }

       
        for key in schema:
            if key not in data or data[key] is None:
                data[key] = schema[key]
            elif isinstance(data[key], list):
                
                if all(isinstance(x, str) for x in data[key]):
                    data[key] = sorted(list(set([x.strip() for x in data[key] if x.strip()])))
                else:
                    
                    data[key] = [x for x in data[key] if x]

        
        langs = data.get("requiredLanguages", [])
        new_langs = []
        for lang in langs:
            if isinstance(lang, str):
                new_langs.append({"name": lang.strip(), "level": "inconnu"})
            elif isinstance(lang, dict):
                name = lang.get("name", "").strip()
                level = lang.get("level", "inconnu").strip()
                if name:
                    new_langs.append({"name": name, "level": level})
        data["requiredLanguages"] = new_langs

        
        educs = data.get("educations", [])
        new_educs = []
        for edu in educs:
            if isinstance(edu, str):
                new_educs.append({"degree": edu.strip(), "field": "inconnu"})
            elif isinstance(edu, dict):
                degree = edu.get("degree", "").strip()
                field = edu.get("field", "inconnu").strip()
                if degree:
                    new_educs.append({"degree": degree, "field": field})
        data["educations"] = new_educs

        return data

    except Exception as e:
        print(f" Erreur Gemini : {e}")
        return None



if __name__ == "__main__":
    print(
        "\n Collez le texte de l'annonce puis :\n"
        "- Ctrl+D (Linux / Mac)\n"
        "- Ctrl+Z puis Entrée (Windows)\n"
    )

    job_text = ""
    try:
        while True:
            job_text += input() + "\n"
    except EOFError:
        pass

    job_text = job_text.strip()
    if not job_text:
        print(" Aucun texte fourni.")
    else:
        result = parse_job_info(job_text)
        if result:
            print("\n === Informations extraites de l'annonce ===\n")
            print(json.dumps(result, indent=4, ensure_ascii=False))
        else:
            print(" Extraction impossible.")
