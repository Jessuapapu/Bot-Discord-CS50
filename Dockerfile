FROM python:3-slim

WORKDIR /app

# Capa de instalacion de dependencias
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Capa de copiado del proyecto
COPY Bot /app/
COPY Reportes /app/Reportes

# Inicializacion de la aplicacion
CMD ["python", "main.py"]