
---

# Pasta Externos

Dentro deste diretório estão os arquivos responsáveis por simular ações dos sensores e atuadores do sistema. Eles desempenham funções essenciais, assinando e publicando em um tópico MQTT para receber e enviar dados e mensagens.

## Funcionalidades

### Simulação de Sensores e Atuadores

Os arquivos contidos neste diretório simulam ações dos sensores e atuadores do sistema. Eles participam ativamente da troca de informações por meio de um tópico MQTT. Essa interação envolve:

1. **Publicação e Assinatura no Tópico MQTT:**
   
    - **Publicação de Dados:** Envia dados e mensagens relevantes para o tópico MQTT, compartilhando informações com outros componentes do sistema.
    
    - **Assinatura de Dados:** Recebe dados e mensagens do tópico MQTT, permitindo a interação com outros elementos do sistema que também estão conectados a esse tópico.

### Conexão via RPC

Além da comunicação por MQTT, o arquivo atuadores.py também está conectados via RPC para tratativas específicas dos dados gerados. Isso implica:

- **Tratamento de Dados:** Utiliza chamadas de procedimento remoto (RPC) para processar e tratar os dados gerados dos sensores e atuadores. Essas tratativas podem envolver transformação ou processamento adicional dos dados antes de serem utilizados pelo sistema.

---
