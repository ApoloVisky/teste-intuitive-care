-- Criação do banco de dados e tabelas
CREATE DATABASE IF NOT EXISTS ans_dados;
USE ans_dados;

-- Tabela de operadoras
CREATE TABLE IF NOT EXISTS operadoras (
    registro_ans VARCHAR(20) PRIMARY KEY,
    cnpj VARCHAR(20),
    razao_social VARCHAR(255),
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(20),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    uf VARCHAR(2),
    cep VARCHAR(10),
    ddd VARCHAR(5),
    telefone VARCHAR(20),
    fax VARCHAR(20),
    email VARCHAR(100),
    representante VARCHAR(255),
    cargo_representante VARCHAR(100),
    data_registro_ans DATE
);

-- Tabela de demonstrações contábeis
CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE,
    registro_ans VARCHAR(20),
    conta VARCHAR(100),
    descricao VARCHAR(255),
    valor DECIMAL(15,2),
    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans)
);