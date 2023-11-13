import json
from multiprocessing import AuthenticationError
import rpyc
from rpyc.utils.server import ThreadedServer
import logging
from dotenv import load_dotenv
import os
import sys
sys.path.append(r'..')
from banco.disponabilidade import VerificadorConexaoDB
from banco.requisicao import BancoDeDados
from middleware.mqtt import MQTT
from middleware.validadores import Validadores

logging.basicConfig(filename='../logs/log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Middleware(rpyc.Service):
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '../bd.env') 
        load_dotenv(dotenv_path)
        PORT = os.getenv("PORT")  
        self.port =  VerificadorConexaoDB(PORT).main()
    def exposed_save_sensor(self, data):
        try:
            dotenv_path = os.path.join(os.path.dirname(__file__), '../bd.env') 
            load_dotenv(dotenv_path)
            user = os.getenv("USERMQTT")
            password = os.getenv("PASSWORDMQTT")   
            conf=self.exposed_get_conf(user, password)
            data_tratados = MQTT(conf).dadosSensor(data)
            self.exposed_post_sens(user, password, json.loads(data_tratados[0]))
            self.exposed_post_atua(user, password,  json.loads(data_tratados[1]))
            return data_tratados[1]
        except Exception as e:
            logging.error(f"[save_sensor] {str(e)}")
            return "Erro de processamento" 
    
    def exposed_tratamentoAtuadores(self,data):
        try:
            mensagem = MQTT().tratamentoAtuadores(data)
            return mensagem
        except Exception as e:
            logging.error(f"[tratamentoAtuadores] {str(e)}")
            return "Erro de processamento"
    
    def exposed_login(self, email, senha):
        try:
            return BancoDeDados(email,senha, self.port).login()
        except Exception as e:
            logging.error(f"[login] {str(e)}")
            return {"erro": str(e)} 

    def exposed_get_conf(self, email, senha):
        try:
            return BancoDeDados(email,senha, self.port).conf('GET')
        except Exception as e:
            logging.error(f"[get_conf] {str(e)}")
            return {"erro": str(e)} 
    
    def exposed_post_conf(self, email, senha, data):
        try:
            data['valorMin'] = valorMin = float(data['valorMin'])
            Validadores().configuracoes(data)
            mapeamento_booleano = {True: 1, False: 0}
            sensorNorte = mapeamento_booleano[data['sensorNorte']]
            sensorSul = mapeamento_booleano[data['sensorSul']]
            sensorLeste = mapeamento_booleano[data['sensorLeste']]
            sensorOeste = mapeamento_booleano[data['sensorOeste']]
            atuaHoriz = mapeamento_booleano[data['atuaHoriz']]
            atuaVert = mapeamento_booleano[data['atuaVert']]
            return BancoDeDados(email,senha, self.port).conf('POST', [valorMin, sensorNorte, sensorSul, sensorLeste, sensorOeste, atuaHoriz, atuaVert])
        except Exception as e:
            logging.error(f"[post_conf] {str(e)}")
            return {"erro": str(e)}

    def exposed_get_atua(self, email, senha):
        try:
            return BancoDeDados(email,senha, self.port).atua('GET')
        except Exception as e:
            logging.error(f"[get_atua] {str(e)}")
            return {"erro": str(e)} 
    
    def exposed_post_atua(self, email, senha, data):
        try:
            Validadores().atuadores(data)
            mapeamento_booleano = {True: 1, False: 0}
            angulo = data['angulo']
            sensor1 = mapeamento_booleano[data['sensor1']]
            sensor2 = mapeamento_booleano[data['sensor2']]
            return BancoDeDados(email,senha, self.port).atua('POST', [sensor1, sensor2, angulo])  
        except Exception as e:
            logging.error(f"[post_atua] {str(e)}")
            return {"erro": str(e)} 
   
    def exposed_get_sens(self, email, senha):
        try:
            return BancoDeDados(email,senha, self.port).sens('GET')
        except Exception as e:
            logging.error(f"[get_sens] {str(e)}")
            return {"erro": str(e)} 
    
    def exposed_post_sens(self, email, senha, data):
        try:
            Validadores().sensores(data)
            norte = data['Norte']
            sul = data['Sul']
            leste = data['Leste']
            oeste = data['Oeste']
            return BancoDeDados(email,senha, self.port).sens('POST', [norte, sul, leste, oeste])   
        except Exception as e:
            logging.error(f"[post_sens] {str(e)}")
            return {"erro": str(e)} 
    
    def exposed_check_connection(self):
        return True
 
def magic_word_authenticator(sock):
    dotenv_path = os.path.join(os.path.dirname(__file__), '../auth.env') 
    load_dotenv(dotenv_path)
    token = os.getenv("SERVIDOR1")
    if sock.recv(64).decode() != token:
        raise AuthenticationError("wrong magic word")
    return sock, None
if __name__ == "__main__":
    ThreadedServer(
    service=Middleware, hostname='localhost',
    port=18862, authenticator=magic_word_authenticator
    ).start()