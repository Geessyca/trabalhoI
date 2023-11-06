import hashlib
import json
import logging
import mysql.connector
from dotenv import load_dotenv
import os

logging.basicConfig(filename='../logs/log.log', level=logging.DEBUG)

class AutenticacaoBD:
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
    def login(self, email, senha):
        try:
            if not self.conn or not self.cursor:
                self.conectar()
            senha_hasheada = hashlib.sha256(senha.encode()).hexdigest()
            consulta = "SELECT * FROM autenticacao WHERE email = %s AND senha = %s"
            valores = (email, senha_hasheada)
            self.cursor.execute(consulta, valores)
            resultado = self.cursor.fetchone()
            if resultado:
                linha_json = {"email":email, "token": senha_hasheada}
                return json.dumps(linha_json, default=str)
            else:
                return False 
        except mysql.connector.Error as e:
            self.logger.error(f"Erro ao executar a consulta: {e}")
            raise

    def get(self, email, senha):
        try:
            if not self.conn or not self.cursor:
                self.conectar()
            consulta = "SELECT * FROM autenticacao WHERE email = %s AND senha = %s"
            valores = (email, senha)
            self.cursor.execute(consulta, valores)
            resultado = self.cursor.fetchone()
            if resultado:
                return True  
            else:
                return False 
        except mysql.connector.Error as e:
            self.logger.error(f"Erro ao executar a consulta: {e}")
            raise

    def post(self, email, senha):
        try:
            if not self.conn:
                self.conectar()

            senha_hasheada = hashlib.sha256(senha.encode()).hexdigest()

            consulta = "INSERT INTO autenticacao (email, senha) VALUES (%s, %s)"
            valores = (email, senha_hasheada)
            self.cursor.execute(consulta, valores)
            self.conn.commit()
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:  
                return False  
            else:
                raise  
        except mysql.connector.Error as e:
            self.logger.error(f"Erro ao inserir dados: {e}")
            raise


