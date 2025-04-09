-- Cria o banco de dados, se ainda não existir
CREATE DATABASE IF NOT EXISTS cpcr;

-- Usa o banco cpcr
USE cpcr;

-- Cria a tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    numero_celular VARCHAR(20),
    senha_hash VARCHAR(255) NOT NULL,
    senha_provisoria BOOLEAN DEFAULT FALSE,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);


