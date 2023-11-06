# server_check_connection.py
import logging
from multiprocessing import AuthenticationError
import os
from dotenv import load_dotenv
import rpyc
from rpyc.utils.server import ThreadedServer
import sys
sys.path.append(r'..')
from middleware.auth import ServidorAuth

logging.basicConfig(filename='../logs/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ConnectionService(rpyc.Service):
    def check_connection_63(self):
        try:
            rpc=ServidorAuth()
            conn = rpc.rpyc_connect('localhost', 18863, authorizer=rpc.token_servidor2())
            response = conn.root.exposed_check_connection()
            if response:
                return conn
            return None
        except Exception as e:
            logging.error("Erro ao verificar a conexão:", e)
            return None
    def check_connection_62(self):
        try:
            rpc=ServidorAuth()
            conn = rpc.rpyc_connect('localhost', 18862, authorizer=rpc.token_servidor1())
            response = conn.root.exposed_check_connection()
            if response:
                return conn
        except Exception as e:
            return self.check_connection_63()

    def connection(self):
        return self.check_connection_62()

    def exposed_save_sensor(self, data):
        conn = self.connection()
        return conn.root.exposed_save_sensor(data)

    def exposed_tratamentoAtuadores(self,data):
        conn = self.connection()
        return conn.root.exposed_tratamentoAtuadores(data)
    
    def exposed_login(self, email, senha):
        conn = self.connection()
        return conn.root.exposed_login(email, senha)

    def exposed_get_conf(self, email, senha):
        conn = self.connection()
        return conn.root.exposed_get_conf(email, senha)
    
    def exposed_post_conf(self, email, senha, data):
        conn = self.connection()
        return conn.root.exposed_post_conf(email, senha, data)

    def exposed_get_atua(self, email, senha):
        conn = self.connection()
        return conn.root.exposed_get_atua(email, senha)
    
    def exposed_post_atua(self, email, senha, data):
        conn = self.connection()
        return conn.root.exposed_post_atua(email, senha, data)
   
    def exposed_get_sens(self, email, senha):
        conn = self.connection()
        return conn.root.exposed_get_sens(email, senha)
    
    def exposed_post_sens(self, email, senha, data):
        conn = self.connection()
        return conn.root.exposed_post_sens(email, senha, data)
    
def magic_word_authenticator(sock):
    dotenv_path = os.path.join(os.path.dirname(__file__), '../auth.env') 
    load_dotenv(dotenv_path)
    token = os.getenv("MIDDLEWARE")
    if sock.recv(64).decode() != token:
        raise AuthenticationError("wrong magic word")
    return sock, None
if __name__ == "__main__":
    ThreadedServer(
    service=ConnectionService, hostname='localhost',
    port=18861, authenticator=magic_word_authenticator
    ).start()
