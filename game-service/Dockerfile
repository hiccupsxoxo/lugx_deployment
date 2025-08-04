# ---- Base image ----
FROM python:3.11-slim

# ---- Working directory ----
WORKDIR /app

# ---- Install dependencies ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy application code ----
COPY . .

# ---- Expose FastAPI port ----
EXPOSE 8085

# ---- Run the FastAPI app ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8085"]
