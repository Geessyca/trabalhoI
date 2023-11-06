
---

# Pasta MQTT

Dentro deste diretório, estão os arquivos necessários para a gestão e administração do protocolo MQTT, permitindo a comunicação entre os diferentes componentes do sistema.

## Detalhes dos Arquivos

### `docker-compose.yaml`

Este arquivo é responsável por orquestrar a inicialização de uma imagem do Mosquitto, um servidor MQTT, na porta 1883. Essa configuração é crucial para estabelecer a infraestrutura de mensagens que permitirá a comunicação assíncrona entre os diversos componentes do sistema.

### `server_mqtt.py`

O arquivo `server_mqtt.py` é responsável por gerenciar as mensagens trocadas nos tópicos utilizados pelos componentes externos localizados na pasta "Externos". Ele coordena e administra as mensagens transmitidas nos tópicos MQTT, permitindo a comunicação entre os diferentes elementos do sistema.

### `auth.py`

Este arquivo é responsável por gerar a configuração de conexão autenticada para o servidor MQTT. Ele garante a autenticação e a configuração segura da conexão entre os diferentes componentes do sistema que utilizam o protocolo MQTT para a troca de informações.

---
