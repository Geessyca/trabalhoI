## Readme - Executando o Projeto

Este documento fornece as instruções necessárias para configurar e executar o projeto.
No arquivo bd.env é possível verificar os dados de acesso ao banco de dados e no auth.env as senhas referente as conexões entre servidors (MQTT, RPC).

### Banco de Dados

Para iniciar o banco de dados, siga os passos abaixo:

1. Na pasta "banco", execute o seguinte comando no terminal para subir o container do Docker:
    ```
    docker-compose up
    ```

2. Após iniciar o container, é necessário abrir um terminal no Docker Desktop ou via linha de comando:

    - **Via Docker Desktop:**
        - Abra o container e clique em "Terminal".

    - **Via Terminal:**
        - Execute o comando `docker ps` para listar os containers ativos.
        - Copie o ID do container do MySQL.
        - Abra o terminal do container via comando Docker Bash:
            ```
            docker exec -it <ID_do_Container> bash
            ```

3. No terminal do container do MySQL, execute os seguintes comandos para configurar e permitir a conexão:

    ```
    mysqld --initialize-insecure
    mysql -u root
    ALTER USER 'root'@'localhost' IDENTIFIED BY 'asdasd';
    FLUSH PRIVILEGES;
    ```

### Teste de Conexão

Após a configuração, teste a conexão via terminal usando o seguinte comando:

```
mysql -u root -p -P 3310
```

Em caso de erro `ERROR 1130 (HY000): Host '***.**.**.*' is not allowed to connect to this MySQL server`, siga os passos abaixo:

1. No terminal do container do MySQL, execute os seguintes comandos para conceder permissões e tente novamente o teste de conexão:

    ```
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'172.22.0.1' IDENTIFIED BY 'asdasd' WITH GRANT OPTION;
    FLUSH PRIVILEGES;
    ```

2. Repita o processo para os dois bancos disponíveis nas portas 3310 e 3311, copiando e executando o arquivo .sql disponível na pasta "banco".

Certifique-se de que a configuração do banco de dados foi bem-sucedida antes de executar o projeto. Estes passos são cruciais para garantir a conectividade adequada do banco de dados ao projeto.

**Observação:** Substitua `<ID_do_Container>` pelo ID real do container do MySQL ao executar os comandos.

Este Readme fornece os passos necessários para configurar e conectar o banco de dados ao projeto. Siga cuidadosamente cada etapa para garantir o funcionamento adequado do sistema.

### Servidor MQTT

Para iniciar o servidor MQTT, siga os passos abaixo:

1. Na pasta "mqtt", execute o seguinte comando no terminal para subir o container do Docker:
    ```
    docker-compose up
    ```

Este comando iniciará o servidor MQTT no container Docker. Certifique-se de que o Docker esteja instalado e funcionando corretamente para executar o comando `docker-compose`.

O servidor MQTT será executado no ambiente configurado pelo Docker.

Certifique-se de que a execução desses comandos esteja ocorrendo na pasta correta, onde está localizado o arquivo `docker-compose.yml` responsável por configurar o ambiente do servidor MQTT.

**Observação:** Certifique-se de que não haja conflitos de portas ou outros serviços já utilizando as portas definidas para o servidor MQTT. Esteja atento a possíveis erros ou avisos durante a inicialização do servidor MQTT.

Este Readme aborda o processo para iniciar o servidor MQTT utilizando Docker Compose. Certifique-se de possuir as permissões necessárias para executar comandos Docker no ambiente em questão.

# Executando os Scripts

Para executar os diferentes componentes do sistema, siga os passos abaixo:

### Middleware

1. **Middleware**:
    - Abra o terminal na pasta "middleware".
    - Execute o comando:
        ```
        python3 main.py
        python3 servidor.py
        python3 servidor2.py
        ```
    Isso iniciará o middleware na porta 18861 e os servidores nas portas 18862 e 18863.

### Controladores/API

2. **Controladores/API**:
    - Na pasta "controladores":
        - Execute os comandos:
            ```
            python3 controlador1.py
            python3 controlador2.py
            ```
    Eles estarão disponíveis na porta 8000 e se conectarão ao middleware.

### MQTT

3. **MQTT**:
    - Na pasta "mqtt":
        - Execute o comando:
            ```
            python3 server_mqtt.py
            ```
    Este comando disponibilizará o servidor na porta 1883 e conectará com o middleware.

### Simuladores

4. **Simuladores**:
    - Na pasta "externos":
        - Execute os comandos:
            ```
            python3 sensores.py
            python3 atuadores.py
            ```
    Eles se conectarão ao middleware e ao MQTT com publicação e assinatura.

### Tela de Interação

5. **Tela de Interação**:
    - Na pasta "cliente":
        - Execute os comandos:
            ```
            npm install
            npm start
            ```
    A aplicação estará disponível na porta 3000 e se conectará via API com a porta 8000.

Certifique-se de ter todas as dependências instaladas e estar utilizando as versões corretas do Python, Node.js (para o npm) e demais bibliotecas necessárias para o correto funcionamento do sistema. Estes comandos inicializam e interconectam os diferentes componentes do sistema para operar de maneira integrada.

Certifique-se de possuir permissões adequadas para execução dos scripts e de estar utilizando os terminais na localização correta, de acordo com as pastas mencionadas.

Lembre-se de verificar possíveis mensagens de erro ou avisos durante a execução dos comandos e corrigir eventuais problemas de configuração ou dependências faltantes.