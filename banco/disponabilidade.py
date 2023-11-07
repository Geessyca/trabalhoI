import threading
from dotenv import load_dotenv
import os
import mysql.connector
import logging
import sys
sys.path.append(r'..')
from banco.sincronizador import TableSync
logging.basicConfig(filename='../logs/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VerificadorConexaoDB:
    def __init__(self, PORT):
        dotenv_path = os.path.join(os.path.dirname(__file__), '../bd.env') 
        load_dotenv(dotenv_path)
        self.host = os.getenv("HOST")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")
        self.port=PORT
        self.port1=os.getenv("PORT1")
        self.port2=os.getenv("PORT2")

    def verificar_conexao(self, porta):
        try:
            cnx = mysql.connector.connect(
                host=self.host,
                port=porta,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cnx.close()
            return True
        except mysql.connector.Error as err:
            logging.error(f"Erro de conexão: {err}")
            return False

    def banco_disponivel(self):
        default = self.verificar_conexao(self.port)
        if not default:
            port1 = self.verificar_conexao(self.port1)
            port2 = self.verificar_conexao(self.port2)
            if port1 and port2:
                logging.info(f"Ambos os bancos de dados estão disponíveis. Usando o banco {self.port1}.")
                self.port= self.port1
            elif port1 and not port2:
                logging.info(f"Usando o banco {self.port1}.")
                self.port= self.port1
            elif port2 and not port1:
                logging.info(f"Usando o banco {self.port2}.")
                self.port= self.port2
            else:
                logging.info("Nenhum banco de dados não está disponível.")
                self.port= None
    
    def main(self):
        self.banco_disponivel()  
        dotenv_path = os.path.join(os.path.dirname(__file__), '../bd.env') 
        load_dotenv(dotenv_path) 
        os.environ["PORT"] = str(self.port)
        return(self.port)