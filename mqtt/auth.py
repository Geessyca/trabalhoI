import os
from dotenv import load_dotenv


class MQTTAuth():
    def __init__(self) -> None:
        pass
    def token(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '../auth.env') 
        load_dotenv(dotenv_path)
        token = os.getenv("MQTT")
        return token.encode()
