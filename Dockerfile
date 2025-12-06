FROM python:3.10-slim

# ------------------------------------
# Diretório de trabalho dentro do container
# ------------------------------------
WORKDIR /app

# ------------------------------------
# Copiar requerimentos e instalar
# ------------------------------------
COPY requirements.txt .

COPY . .

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------------
# Porta e comando de inicialização
# ------------------------------------
EXPOSE 5000
#CMD ["python", "app.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]

