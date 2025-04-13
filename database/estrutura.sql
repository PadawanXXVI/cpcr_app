-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS cr_novacap CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cpcr;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    numero_celular VARCHAR(20),
    senha_hash TEXT NOT NULL,
    aprovado BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de processos
CREATE TABLE IF NOT EXISTS processos (
    id_processo INT AUTO_INCREMENT PRIMARY KEY,
    numero_processo VARCHAR(25) NOT NULL UNIQUE,
    data_criacao_ra DATE NOT NULL,
    tramite_inicial VARCHAR(10) NOT NULL,
    data_entrada DATE NOT NULL,
    admin_regional VARCHAR(100) NOT NULL,
    tipo_demanda VARCHAR(100) NOT NULL,
    vistoria_completa VARCHAR(10),
    diretoria_destino VARCHAR(10),
    status_demanda VARCHAR(100) NOT NULL,
    descricao_processo TEXT,
    data_ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de movimentações
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

-- Tabela de logs
CREATE TABLE IF NOT EXISTS logs (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    acao VARCHAR(200),
    ip_maquina VARCHAR(45),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Tabela de status
CREATE TABLE IF NOT EXISTS status (
    id_status INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL
);

-- Tabela de demandas
CREATE TABLE IF NOT EXISTS demandas (
    id_demanda INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL
);

-- Tabela de regiões administrativas
CREATE TABLE IF NOT EXISTS regioes_administrativas (
    id_ra INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL,
    nome VARCHAR(100) NOT NULL
);

-- Inserção de STATUS
INSERT INTO status (nome) VALUES
("Enviado à Diretoria das Cidades"),
("Enviado à Diretoria de Obras"),
("Devolvido à RA de origem"),
("Improcedente - tramitação pelo SGIA"),
("Improcedente - implantação ou necessita de orçamento próprio"),
("Improcedente - cronograma próprio da Diretoria"),
("Concluído");

-- Inserção de DEMANDAS
INSERT INTO demandas (nome) VALUES
("Tapa-buraco"),
("Boca de Lobo"),
("Bueiro"),
("Calçada"),
("Estacionamentos"),
("Galeria de Águas Pluviais"),
("Jardim"),
("Mato Alto"),
("Meio-fio"),
("Parque Infantil"),
("Passagem Subterrânea"),
("Passarela"),
("Pisos Articulados"),
("Pista de Skate"),
("Ponto de Encontro Comunitário (PEC)"),
("Praça"),
("Quadra de Esporte"),
("Rampa"),
("Alambrado (Cercamento)"),
("Implantação (calçada, quadra, praça, estacionamento etc.)"),
("Recapeamento Asfáltico"),
("Poda / supressão de árvore"),
("Doação de mudas");

-- Inserção das RAs
INSERT INTO regioes_administrativas (codigo, nome) VALUES
("RA I", "Plano Piloto"),
("RA II", "Gama"),
("RA III", "Taguatinga"),
("RA IV", "Brazlândia"),
("RA V", "Sobradinho"),
("RA VI", "Planaltina"),
("RA VII", "Paranoá"),
("RA VIII", "Núcleo Bandeirante"),
("RA IX", "Ceilândia"),
("RA X", "Guará"),
("RA XI", "Cruzeiro"),
("RA XII", "Samambaia"),
("RA XIII", "Santa Maria"),
("RA XIV", "São Sebastião"),
("RA XV", "Recanto das Emas"),
("RA XVI", "Lago Sul"),
("RA XVII", "Riacho Fundo"),
("RA XVIII", "Lago Norte"),
("RA XIX", "Candangolândia"),
("RA XX", "Águas Claras"),
("RA XXI", "Riacho Fundo II"),
("RA XXII", "Sudoeste/Octogonal"),
("RA XXIII", "Varjão"),
("RA XXIV", "Park Way"),
("RA XXV", "SCIA/Estrutural"),
("RA XXVI", "Sobradinho II"),
("RA XXVII", "Jardim Botânico"),
("RA XXVIII", "Itapoã"),
("RA XXIX", "SIA"),
("RA XXX", "Vicente Pires"),
("RA XXXI", "Fercal"),
("RA XXXII", "Sol Nascente e Pôr do Sol"),
("RA XXXIII", "Arniqueira"),
("RA XXXIV", "Arapoanga"),
("RA XXXV", "Água Quente");
