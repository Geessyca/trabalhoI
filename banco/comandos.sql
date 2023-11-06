CREATE DATABASE sd;
USE sd;

CREATE TABLE sensores (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Norte FLOAT,
    Sul FLOAT,
    Leste FLOAT,
    Oeste FLOAT
);
 

SELECT * FROM atuadores;

CREATE TABLE atuadores (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sensor1 BOOLEAN,
    sensor2 BOOLEAN,
    angulo INT CHECK (angulo IN (-20, 0, 20))
);

SELECT * FROM atuadores;

CREATE TABLE configuracoes (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    Data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valorMin FLOAT,
    sensorNorte BOOLEAN,
    sensorSul BOOLEAN,
    sensorLeste BOOLEAN,
    sensorOeste BOOLEAN,
    atuaHoriz BOOLEAN,
    atuaVert BOOLEAN
);

SELECT * FROM configuracoes;

CREATE TABLE autenticacao (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);
INSERT INTO autenticacao (email, senha) 
VALUES ('mqtt', '456f37aa91aa3a4b2a6ebe5f2a86aab6cb98250a1f9d78da96d0d6fac78d4128');

SELECT * FROM autenticacao;
