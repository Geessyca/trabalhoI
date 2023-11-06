
---

# Pasta Middleware

Neste diretório estão os principais componentes responsáveis pela intermediação, validação e tratamento das chamadas no sistema. Cada arquivo desempenha funções específicas, garantindo a operacionalidade e disponibilidade do sistema.

## Detalhes dos Arquivos

### `main.py`

Este arquivo contém um servidor RPC que age como intermediário para outros dois servidores. Sua função principal é validar a disponibilidade para garantir a operação contínua do sistema.

### `servidor.py` e `servidor2.py`

Ambos os arquivos são servidores RPC responsáveis por intermediar as chamadas, tratativas e operações relacionadas ao banco de dados. Suas funções abrangem o processamento das solicitações e garantem que sejam tratadas corretamente antes de serem encaminhadas para o banco de dados.

### `mqtt.py`

O arquivo `mqtt.py` contém tratativas relacionadas às requisições feitas pelos tópicos MQTT. Este componente lida com a comunicação e interações realizadas através do protocolo MQTT, possibilitando o envio e recebimento de dados relevantes para o sistema.

### `validadores`

Esta pasta contém scripts ou módulos responsáveis por validar as requisições `POST` feitas via API. Eles garantem a integridade e autenticidade dos dados submetidos ao sistema, assegurando que estejam em conformidade com os critérios estabelecidos.

### `auth.py`

Este arquivo é responsável por gerar a configuração de conexão autenticada para o servidor RPC. Ele garante a autenticação e a configuração segura da conexão entre os diferentes componentes do sistema que utilizam o protocolo RPC para a troca de informações.

---
