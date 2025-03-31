# Testes de Nivelamento

Este repositório contém soluções para os testes de nivelamento propostos, abrangendo diversas áreas da tecnologia, incluindo Web Scraping, Transformação de Dados, Banco de Dados e Desenvolvimento de APIs.

## 📌 Índice

- [📖 Sobre o Projeto](#sobre-o-projeto)
- [⚙️ Pré-requisitos](#pré-requisitos)
- [📥 Clonando o Repositório](#clonando-o-repositório)
- [📦 Instalando Dependências](#instalando-dependências)
- [🚀 Execução dos Testes](#execução-dos-testes)
  - [🕵️‍♂️ 1. Teste de Web Scraping](#1-teste-de-web-scraping)
  - [🗂️ 2. Teste de Transformação de Dados](#2-teste-de-transformação-de-dados)
  - [🗄️ 3. Teste de Banco de Dados](#3-teste-de-banco-de-dados)
  - [🌐 4. Teste de API](#4-teste-de-api)
- [🛠️ Coleção do Postman](#coleção-do-postman)
- [📬 Contato](#contato)

## 📖 Sobre o Projeto

O objetivo deste projeto é fornecer soluções práticas para testes técnicos de nivelamento, demonstrando habilidades em diferentes áreas do desenvolvimento de software. Cada teste está contido em seu respectivo diretório, com instruções específicas para execução.

## ⚙️ Pré-requisitos

Antes de iniciar, certifique-se de ter os seguintes softwares instalados em sua máquina:

- ✅ [Python 3.8 ou superior](https://www.python.org/downloads/) 🐍
- ✅ [Git](https://git-scm.com/downloads) 🛠️
- ✅ [Docker e Docker Compose](https://www.docker.com/get-started) 🐳
- ✅ [Node.js e npm](https://nodejs.org/en/download/) 📦

## 📥 Clonando o Repositório

Para obter uma cópia local do projeto, execute os seguintes comandos no terminal:

```bash
git clone https://github.com/ApoloVisky/teste-intuitive-care.git
cd teste-intuitive-care
```

## 📦 Instalando Dependências

Navegue até o diretório raiz do projeto e instale as dependências Python necessárias:

```bash
pip install -r requirements.txt
```

## 🚀 Execução dos Testes

### 🕵️‍♂️ 1. Teste de Web Scraping

Este teste envolve a extração de dados de páginas web.

📌 **Execução:**

```bash
python teste1WebScraping.py
```

### 🗂️ 2. Teste de Transformação de Dados

Este teste foca na manipulação e transformação de dados de arquivos CSV.

📌 **Execução:**

```bash
python teste2Csv.py
```

### 🗄️ 3. Teste de Banco de Dados

Este teste abrange a criação e manipulação de um banco de dados utilizando Docker.

📌 **Passos:**

1️⃣ **Navegue até o diretório do teste:**

```bash
cd teste3
```

2️⃣ **Inicie o banco de dados com Docker Compose:**

```bash
docker-compose up -d
```

3️⃣ **Execute o script para configurar o banco de dados e realizar as operações necessárias:**

```bash
python teste3_bancoDeDados.py
```

### 🌐 4. Teste de API

Este teste envolve o desenvolvimento e consumo de uma API, incluindo a configuração do backend e frontend.

📌 **Passos:**

1️⃣ **Navegue até o diretório do teste:**

```bash
cd teste4
```

2️⃣ **Inicie o backend:**

- Navegue até o diretório do backend:

  ```bash
  cd backend
  ```

- Inicie o servidor:

  ```bash
  python server.py
  ```

3️⃣ **Inicie o frontend:**

- Abra um novo terminal e navegue até o diretório do frontend:

  ```bash
  cd frontend
  ```

- Instale as dependências:

  ```bash
  npm install
  ```

- Inicie o servidor frontend:

  ```bash
  npm run serve
  ```

📍 A aplicação estará disponível em: **`http://localhost:8080/`** 🌍

## 🛠️ Coleção do Postman

Para facilitar os testes da API, uma coleção do Postman foi preparada.

📌 **Importação da Coleção:**

1️⃣ **Abra o Postman.**
2️⃣ **Vá em "File" > "Import".**
3️⃣ **Selecione o arquivo `Teste_Api_collection.json` localizado no diretório raiz do projeto.**
4️⃣ **Após a importação, você poderá utilizar as requisições pré-configuradas para interagir com a API.**

## 📬 Contato

Caso tenha dúvidas, entre em contato:

📧 **E-mail:** adeilton.s.polovodoff@gmail.com
🐙 **GitHub:** [ApoloVisky](https://github.com/ApoloVisky)  


