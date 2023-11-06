import datetime
import json
import logging
import mysql.connector
from dotenv import load_dotenv
import os

logging.basicConfig(filename='../logs/log.log', level=logging.DEBUG)

class SensoresBD:
    def __init__(self, port):
        dotenv_path = os.path.join(os.path.dirname(__file__), '../../bd.env') 
        load_dotenv(dotenv_path)
        self.host = os.getenv("HOST")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")
        self.port = port
        self.conn = None
        self.cursor = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            self.logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def desconectar(self):
        if self.conn:
            self.conn.close()
        if self.cursor:
            self.cursor.close()

    def get(self,):
        try:
            if not self.conn or not self.cursor:
                self.conectar()
            query = "SELECT * FROM sensores ORDER BY Data DESC LIMIT 30"
            self.cursor.execute(query)
            colunas = [coluna[0] for coluna in self.cursor.description]
            resultados = self.cursor.fetchall()
            lista_json = []
            for resultado in resultados:
                linha_json = {}
                for i, valor in enumerate(resultado):
                    if isinstance(valor, datetime.datetime) and colunas[i] == 'Data':
                        linha_json[colunas[i]] = valor.strftime('%Y-%m-%dT%H:%M:%S')
                    else:
                        linha_json[colunas[i]] = valor
                lista_json.append(linha_json)

            return json.dumps(lista_json, default=str)
        except mysql.connector.Error as e:
            self.logger.error(f"Erro ao executar a consulta: {e}")
            raise

    def post(self, norte, sul, leste, oeste):
        try:
            if not self.conn:
                self.conectar()

            consulta = "INSERT INTO sensores (Norte, Sul, Leste, Oeste) VALUES (%s, %s, %s, %s)"
            valores = (norte, sul, leste, oeste)
            self.cursor.execute(consulta, valores)
            self.conn.commit()
        except mysql.connector.Error as e:
            self.logger.error(f"Erro ao inserir dados: {e}")
            raise


