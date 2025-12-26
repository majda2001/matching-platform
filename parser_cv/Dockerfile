FROM python:3.11-slim

WORKDIR /app

# Installer dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Port exposé
EXPOSE 8001

# Lancer FastAPI
CMD ["uvicorn", "main_cv:app", "--host", "0.0.0.0", "--port", "8001"]
