
---

# Pasta Controladores

Este diretório abriga dois controladores Flask, os quais desempenham um papel crucial na intermediação entre o front-end e o sistema. A interação entre o front-end e esses controladores é realizada por meio de uma API para o lado do cliente e via RPC (Remote Procedure Call) para os servidores responsáveis pela conexão com o banco de dados e por tratativas necessárias.

## Detalhes dos Controladores

### Arquitetura

Ambos os controladores são desenvolvidos em Flask, um framework web em Python, e são configurados para atuar na porta 8000. Essa configuração permite que, em caso de falha em um dos controladores, o outro assuma as operações, garantindo uma maior disponibilidade do sistema.

### Funcionalidades

1. **Interação com o Front-end via API:**

    Os controladores atuam como uma interface entre o front-end e o sistema, permitindo requisições e respostas por meio de uma API. Essas solicitações são tratadas e processadas para atender às necessidades do cliente.

2. **Comunicação com Servidores de Banco de Dados via RPC:**

    Além da interação com o front-end, os controladores utilizam chamadas de procedimento remoto (RPC) para se comunicar com os servidores responsáveis pela conexão com o banco de dados. Isso permite que os dados sejam gerenciados e processados de acordo com as demandas do sistema, garantindo a integridade e segurança dos dados.

---
