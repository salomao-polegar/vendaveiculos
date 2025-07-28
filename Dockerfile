# Usa imagem base com Python 3.12
FROM python:3.12-slim

# Variáveis de ambiente básicas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container
WORKDIR /app

# Instala pacotes de sistema necessários
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos do projeto para o container
COPY . /app/

# Instala dependências Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Executa migrações e inicia o servidor com gunicorn
CMD bash -c "python manage.py migrate && \
             python manage.py collectstatic --noinput && \
             gunicorn loja_de_veiculos.wsgi:application --bind 0.0.0.0:8000"
