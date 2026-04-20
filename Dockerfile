FROM python:3.11-slim

WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para arrancar
CMD ["uvicorn", "agent.main:app", "--host", "0.0.0.0", "--port", "8000"]
