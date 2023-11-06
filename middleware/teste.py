import base64
import json
import rpyc
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
sys.path.append(r'..')
from middleware.auth import MiddlewareAuth


rpc=MiddlewareAuth()
conn = rpc.rpyc_connect('localhost', 18861, authorizer=rpc.token())
api_service = conn.root

resultado = api_service.exposed_login("gessyca@email.com","123456")
print(resultado)