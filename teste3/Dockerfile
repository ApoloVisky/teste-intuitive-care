# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MYSQL_HOST=mysql
ENV MYSQL_PORT=3306
ENV MYSQL_DATABASE=ans_dados
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=admin123

# Criar e definir o diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt primeiro para aproveitar o cache de camadas
COPY requirements.txt .

# Instalar dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto dos arquivos da aplicação
COPY . .

# Criar diretório para dados
RUN mkdir -p /app/dados_ans

# Comando para executar a aplicação
CMD ["python", "teste3_bancoDeDados.py"]