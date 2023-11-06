import os
from dotenv import load_dotenv
import rpyc

class AuthSocketStream(rpyc.SocketStream):

    @classmethod
    def connect(cls, *args, authorizer=None, **kwargs):
        stream_obj =  super().connect(*args, **kwargs)

        if callable(authorizer):
            authorizer(stream_obj.sock)

        return stream_obj

class MiddlewareAuth():
    def __init__(self) -> None:
        pass
    def token(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '../auth.env') 
        load_dotenv(dotenv_path)
        token = os.getenv("MIDDLEWARE")
        return lambda sock: sock.send(token.encode())
    def rpyc_connect(self,host, port, service=rpyc.VoidService, config={}, ipv6=False, keepalive=False, authorizer=None):
        s = AuthSocketStream.connect(
                host, port, ipv6=ipv6, keepalive=keepalive,
                authorizer=authorizer
        )

        return rpyc.connect_stream(s, service, config)
    
class ServidorAuth():
    def __init__(self) -> None:
        pass
    def token(self, servidor):
        dotenv_path = os.path.join(os.path.dirname(__file__), '../auth.env') 
        load_dotenv(dotenv_path)
        token = os.getenv(servidor)
        return token
    
    def token_servidor1(self):
        token=self.token("SERVIDOR1")
        return lambda sock: sock.send(token.encode())
    
    def token_servidor2(self):
        token=self.token("SERVIDOR2")
        return lambda sock: sock.send(token.encode())
    
    def rpyc_connect(self,host, port, service=rpyc.VoidService, config={}, ipv6=False, keepalive=False, authorizer=None):
        s = AuthSocketStream.connect(
                host, port, ipv6=ipv6, keepalive=keepalive,
                authorizer=authorizer
        )

        return rpyc.connect_stream(s, service, config)