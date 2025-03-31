# Testes de Nivelamento

Este repositório contém a solução para os testes de nivelamento propostos no documento.


Para iniciar o projeto dê o comando git clone https://github.com/ApoloVisky/teste-intuitive-care

Para iniciar a execução do teste digite o comando pip install -r requirements.txt para instalar todas as dependências

## 1. Teste de Web Scraping

Digite o comando python teste1WebScraping.py no terminal para o primeiro teste


## 2. Teste de Transformação de Dados

Digite o comando python teste2Csv.py no terminal para o segundo teste

## 3. Teste de Banco de dados

Para iniciar digite no terminal: cd teste3.

Para subir o banco de dados Docker no terminal digite: docker-compose up

Para executar o teste, no terminal digite: teste3_bancoDeDados.py

Esse comando irá criar o banco de dados junto com as tabelas, realizar a importação dos dados do Csv baixado e realizar as querys desejadas

## 4. Teste de api

Digite cd backend no terminal
Após isso inicie o back end com o comando python server.py
Abra outro terminal

Digite cd frontend no terminal

Após isso digite npm intall para instalar as dependências

Para iniciar o servidor: npm run serve.
O mesmo estará disponível na porta http://192.168.15.6:8080/ para efetuar as buscas

## Postman Collection

Para testar a API no Postman, importe a coleção localizada em:

📂 `Teste_Api_collection.json`

### Como importar:
1. Abra o Postman.
2. Vá em **File > Import**.
3. Selecione o arquivo `Teste_Api_collection.json`.
4. Teste as requisições!


