<h1 align="center">
  🎓<br>Sistema Distribuido - Melhoria na captação de energia solar
</h1>

<h4 align="center">
O intuito deste repositório é compartilhar o código criado para a matéria de sistema distribuido.
</h4>

---

### Sobre o projeto 

O projeto tem como foco a implementação de um sistema para otimizar a captação de energia solar. Ele se baseia na coleta de dados de quatro sensores de radiação solar, e utiliza dois atuadores para ajustar a placa solar em ângulos que variam de -20 a 20 graus, tanto na horizontal quanto na vertical. Isso assegura o posicionamento ideal da placa, direcionando-a para onde a incidência solar é mais significativa.

O algoritmo foi desenvolvido em Python para o servidor, utilizando tecnologias como RPC, MQTT e API. Além disso, o frontend foi construído com ReactJS, proporcionando uma interface para a visualização dos dados coletados e permitindo configurações personalizadas.


### Arquitetura 

Para acessar o sistema, o cliente utiliza uma interface interativa (front-end) que se conecta via API ao controlador. O acesso é protegido por um autenticador por e-mail e senha, o qual protege todas as rotas do sistema.

O nosso controlador é projetado com redundância para garantir a disponibilidade do sistema. Ele se conecta ao nosso Middleware, que realiza comunicação via RPC, também com redundância. Essa comunicação é responsável pelo envio e coleta de dados em nosso banco de dados MySQL.

É importante destacar que nosso banco de dados também é construído com redundância. Além disso, implementamos um algoritmo de sincronização que assegura a consistência entre as réplicas do banco de dados.

Os dados gerados pelo sistema são fictícios e gerados aleatoriamente, variando de 0 a 50. Para simular erros nos dados, definimos que todos os números acima de 38 são registrados como nulos (None). A transmissão desses dados é realizada via MQTT, também com autenticação. O simulador do atuador recebe os dados relacionados aos sensores que devem ser ajustados e a posição angular. Além disso, implementamos um script no atuador que normaliza as mensagens, realizando esse processo via Middleware.

Todos os dados publicados via MQTT são inseridos no nosso banco de dados, sendo posteriormente consumidos pela nossa API e frequentemente visualizados pelo nosso frontend.


---

A seguir, é possível visualizar as configurações necessárias para executar a aplicação, juntamente com as instruções para executar cada script. Cada cenário está localizado em uma pasta separada, identificada pelo nome correspondente a ele. Dentro de cada pasta, você encontrará um arquivo README que contém informações sobre as responsabilidades de cada script.

## Configurações do Projeto

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
---

Certifique-se de ter todas as dependências instaladas e estar utilizando as versões corretas do Python, Node.js (para o npm) e demais bibliotecas necessárias para o correto funcionamento do sistema. Estes comandos inicializam e interconectam os diferentes componentes do sistema para operar de maneira integrada.

Certifique-se de possuir permissões adequadas para execução dos scripts e de estar utilizando os terminais na localização correta, de acordo com as pastas mencionadas.

Lembre-se de verificar possíveis mensagens de erro ou avisos durante a execução dos comandos e corrigir eventuais problemas de configuração ou dependências faltantes.

##  👩🏻‍💻 Autora<br>
<table>
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/geessyca/">
        <img src="https://avatars.githubusercontent.com/u/72661229?v=4" width="100px;" alt="Icon GitHub"/><br>
        <sub>
          <b>Gessyca Moreira</b>
        </sub>
      </a>
    </td>
  </tr>
</table>