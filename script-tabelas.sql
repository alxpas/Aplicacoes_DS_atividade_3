-- Criação das tabelas para no Supabase --

-- Criação da tabela de Clientes
CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Criação da tabela de Destinos
CREATE TABLE destinos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL
);

-- Criação da tabela de Vendas (Tabela associativa)
CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    destino_id INTEGER NOT NULL,
    data_viagem DATE NOT NULL,
    -- Definindo as chaves estrangeiras
    CONSTRAINT fk_cliente
        FOREIGN KEY (cliente_id) 
        REFERENCES clientes (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_destino
        FOREIGN KEY (destino_id) 
        REFERENCES destinos (id)
        ON DELETE CASCADE
);