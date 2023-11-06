
---

# Pasta Banco de Dados

Esta pasta contém scripts e arquivos relacionados à gestão e sincronização de dois bancos de dados MySQL em portas diferentes.

## Arquivos

### docker-compose.yml

Arquivo responsável por configurar e iniciar os bancos de dados MySQL. Utiliza o Docker e cria dois contêineres nas portas 3310 e 3311.

### comandos.sql

Contém os comandos SQL necessários para inicializar os bancos de dados, incluindo a criação de tabelas e outras configurações.

### disponabilidade.py

Um script em Python que verifica a disponibilidade das portas dos bancos de dados. Por padrão, retorna a porta 3310 se ambas estiverem disponíveis. Além disso, este script chama o arquivo `sincronizador.py`, responsável por sincronizar os dados entre os dois bancos. Essas ações de verificação e sincronização ocorrem a cada 30 segundos.

### sincronizador.py

Script encarregado de sincronizar os dados entre os dois bancos de dados. Este arquivo é chamado pelo `disponabilidade.py` e executa a sincronização em intervalos regulares.

### requisicao.py

Este script centraliza as conexões aos bancos de dados e solicitações às tabelas. Cada tabela possui seu próprio script para operações de inserção ou seleção de dados, armazenados na pasta `request`.

## Pasta Request

Contém scripts de solicitação para cada tabela presente nos bancos de dados. Cada arquivo dentro desta pasta executa operações específicas, como inserção ou seleção de dados em tabelas específicas.

---
