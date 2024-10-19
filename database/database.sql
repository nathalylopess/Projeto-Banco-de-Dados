CREATE DATABASE IF NOT EXISTS genrenciador_tarefas;
USE genrenciador_tarefas;

CREATE TABLE IF NOT EXISTS tb_usuarios (
    usu_id INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
    usu_nome VARCHAR(200) NOT NULL,
    usu_email VARCHAR(200) NOT NULL,
    usu_senha VARCHAR(200) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_tarefas (
    tar_id INT(11) AUTO_INCREMENT PRIMARY KEY NOT NULL,
    tar_status VARCHAR(50) NOT NULL,
    tar_data DATE NOT NULL,
    tar_prazo DATE NOT NULL,
    tar_prioridade VARCHAR(50) NOT NULL,
    tar_descricao TEXT NOT NULL, 
    tar_categoria VARCHAR(100) NOT NULL
);