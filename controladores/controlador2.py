import base64
import json
import rpyc
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
sys.path.append(r'..')
from middleware.auth import MiddlewareAuth


app = Flask('app')
CORS(app)

rpc=MiddlewareAuth()
conn = rpc.rpyc_connect('localhost', 18861, authorizer=rpc.token())
api_service = conn.root

def credenciais(auth_header):
    if not auth_header:
        raise ValueError('Credenciais não fornecidas.')
    if auth_header.startswith('Basic '):
        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        return decoded_credentials.split(':')
    raise ValueError('Credenciais inválidas.')

def retornos(retorno):  
    if 'erro' in retorno or 'success' in retorno:
        if str(retorno) == "{'success': 'Salvo'}":
            return jsonify({'success': 'Salvo'}), 200
        elif str(retorno) == "{'success': 'Autenticado'}":
            return jsonify({'success': 'Autenticado'}), 200
        elif str(retorno) == "{'erro': 'Requisicao inválido'}":
            return jsonify({'erro': 'Requisicao inválido'}), 400
        elif str(retorno) == "{'erro': 'Credenciais inválidas}":
            return jsonify({'erro': 'Credenciais inválidas'}), 401
        elif str(retorno) == "{'erro': 'Usuario ou senha invalido}":
             return jsonify({'erro': 'Usuario ou senha invalido'}), 401
        else:
            return jsonify({'erro':retorno['erro']}), 400
    return json.loads(retorno), 200


@app.route('/api/get/conf', methods=['GET'])
def get_conf():
    if request.method == 'GET':
        try:
            email, senha = credenciais(request.headers.get('Authorization'))
            resultado = api_service.exposed_get_conf(email, senha)
            return retornos(resultado)
        except ValueError as e:
            return jsonify({'erro': str(e)}), 401
        except Exception as e:
            return jsonify({'erro': str(e)}), 400
    else:
        return jsonify({'erro': 'Método inválido'}), 405
        
@app.route('/api/post/conf', methods=['POST'])
def post_conf(): 
    if request.method == 'POST':
        try:
            email, senha = credenciais(request.headers.get('Authorization'))
            data=request.get_json()
            resultado = api_service.exposed_post_conf(email, senha, data)
            return retornos(resultado)
        except Exception as e: 
            return jsonify({'erro': str(e)}), 400
    else:
        return jsonify({'erro': 'Método inválido'}), 405
    
@app.route('/api/get/atua', methods=['GET'])
def get_atua():
    if request.method == 'GET':
        try:
            email, senha = credenciais(request.headers.get('Authorization'))
            resultado = api_service.exposed_get_atua(email, senha)
            return retornos(resultado)
        except ValueError as e:
            return jsonify({'erro': str(e)}), 401
        except Exception as e:
            return jsonify({'erro': str(e)}), 400
    else:
        return jsonify({'erro': 'Método inválido'}), 405

@app.route('/api/get/sens', methods=['GET'])
def get_sens():
    if request.method == 'GET':
        try:
            email, senha = credenciais(request.headers.get('Authorization'))
            resultado = api_service.exposed_get_sens(email, senha)
            return retornos(resultado) 
        except ValueError as e:
            return jsonify({'erro': str(e)}), 401
        except Exception as e:
            return jsonify({'erro': str(e)}), 400
    else:   
        return jsonify({'erro': 'Método inválido'}), 405

        
@app.route('/api/login', methods=['POST'])
def login(): 
    if request.method == 'POST':
        try:
            data=request.get_json()
            resultado = api_service.exposed_login(data["email"], data["senha"])
            return retornos(resultado)
        except Exception as e: 
            return jsonify({'erro': str(e)}), 400
    else:
        return jsonify({'erro': 'Método inválido'}), 405

if __name__ == '__main__':
    app.run(debug=True, port=8000)