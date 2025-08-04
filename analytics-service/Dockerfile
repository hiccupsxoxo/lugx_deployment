# Use Python 3.11 slim as the base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the FastAPI service port
EXPOSE 8087

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8087"]
