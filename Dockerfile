# Imagen base
FROM python:3.9-slim

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar los archivos de la aplicación al contenedor
COPY . /app

# Instalar las dependencias
RUN apt-get update && apt-get install -y gcc libpq-dev

RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 5000 para acceder a la aplicación Flask
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "./src/app.py"]
