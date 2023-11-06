import json
import sys

from flask import jsonify
sys.path.append(r'D:\sd\trabalhoI')
from banco.request.autenticacao import AutenticacaoBD
from banco.request.atuadores import AtuadoresBD
from banco.request.configuracoes import ConfiguracoesBD
from banco.request.sensores import SensoresBD

class BancoDeDados:
    def __init__(self, user, password, port):
        self.user = user
        self.password = password
        self.port = port      
        self.auth = self.permissao()  
           
    def permissao(self):
        try:
            autenticacao_db = AutenticacaoBD(self.port)
            resposta= autenticacao_db.get(self.user, self.password)
            return resposta
        except Exception as e:
            return f"Ocorreu um erro: {e}"
        finally:
            autenticacao_db.desconectar()
    
    def login(self):
        try:
            autenticacao_db = AutenticacaoBD(self.port)
            resposta= autenticacao_db.login(self.user, self.password)
            if resposta:
                return resposta
            else:
                return {"erro":"Usuario ou senha invalido"}
        except Exception as e:
            return f"Ocorreu um erro: {e}"
        finally:
            autenticacao_db.desconectar()

    def conf(self, metodo, data=[]):
        if self.auth:
            configuracoes_db = ConfiguracoesBD(self.port)
            try:
                if metodo=='GET':
                    resposta= configuracoes_db.get()
                    return resposta
                elif metodo =='POST' and len(data) == 7:
                    resposta = configuracoes_db.post(data[0], data[1], data[2], data[3], data[4], data[5],data[6])
                    return {"success": "Salvo"}
                else:
                    return {"erro": "Requisicao inválido"}
            except Exception as e:
                return f"Ocorreu um erro: {e}"
            finally:
                configuracoes_db.desconectar()
        else:
            return {"erro": "Credenciais invalidas."}
        
    def atua(self, metodo, data=[]):
        if self.auth:
            atuadores_db = AtuadoresBD(self.port)
            try:
                if metodo=='GET':
                    resposta= atuadores_db.get()
                    return resposta
                elif metodo =='POST'and len(data) == 3:
                    resposta = atuadores_db.post(data[0], data[1], data[2])
                    return {"success": "Salvo"}
                else:
                    return {"erro": "Requisicao inválido"}
            except Exception as e:
                return f"Ocorreu um erro: {e}"
            finally:
                atuadores_db.desconectar()
        else:
            return {"erro": "Credenciais invalidas."}
   
    def sens(self, metodo, data=[]):
        if self.auth:
            sensores_db = SensoresBD(self.port)
            try:
                if metodo=='GET':
                    resposta= sensores_db.get()
                    return resposta
                elif metodo =='POST'and len(data) == 4:
                    resposta = sensores_db.post(data[0], data[1], data[2], data[3])
                    return {"success": "Salvo"}
                else:
                    return {"erro": "Requisicao inválido"}
            except Exception as e:
                 return f"Ocorreu um erro: {e}"
            finally:
                sensores_db.desconectar()
        else:
            return {"erro": "Credenciais invalidas."}

    def criar_usuario(self):
        try:
            autenticacao_db = AutenticacaoBD(self.port)
            autenticacao_db.post(self.user, self.password)
            return {"success": "Salvo"}
        except Exception as e:
            return f"Ocorreu um erro: {e}"
        finally:
            autenticacao_db.desconectar()