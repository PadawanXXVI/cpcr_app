-- Cria o banco de dados (se não existir)
CREATE DATABASE IF NOT EXISTS cpcr;
USE cpcr;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    numero_celular VARCHAR(20),
    senha_hash TEXT NOT NULL,
    senha_provisoria BOOLEAN DEFAULT FALSE,
    aprovado BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    senha_expira_em DATE,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de processos
CREATE TABLE IF NOT EXISTS processos (
    id_processo INT AUTO_INCREMENT PRIMARY KEY,
    numero_processo VARCHAR(25) NOT NULL UNIQUE,
    data_criacao_ra DATE NOT NULL,
    data_entrada_cpcr DATE NOT NULL,
    admin_regional VARCHAR(100) NOT NULL,
    tipo_demanda VARCHAR(100) NOT NULL,
    vistoria_completa TEXT,
    diretoria_destino VARCHAR(10),
    status_demanda VARCHAR(100) NOT NULL,
    descricao_processo TEXT,
    data_ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de movimentações (histórico de atualizações)
CREATE TABLE IF NOT EXISTS movimentacoes (
    id_movimentacao INT AUTO_INCREMENT PRIMARY KEY,
    id_processo INT NOT NULL,
    id_usuario INT NOT NULL,
    data_movimentacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_movimentado VARCHAR(100) NOT NULL,
    observacoes TEXT,
    FOREIGN KEY (id_processo) REFERENCES processos(id_processo),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);
