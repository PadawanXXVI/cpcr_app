-- Cria o banco de dados, se ainda não existir
CREATE DATABASE IF NOT EXISTS cpcr;

-- Usa o banco cpcr
USE cpcr;

-- Cria a tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    numero_celular VARCHAR(20),
    senha_hash TEXT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    senha_expira_em DATE
);
