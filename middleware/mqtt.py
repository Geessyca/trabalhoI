import json
import re
class MQTT:
    def __init__(self, conf=None):
        self.conf=conf
        pass

    def tratamento(self,dados):
        dados_tratados = re.findall(r'\[.*?\]|\d+|None', str(dados))
        if len(dados_tratados) == 1:
            dados_tratados = re.findall(r'\d+|None', dados_tratados[0])
            dados_tratados = [int(s) if s.isdigit() else -1 if s == 'None' else s for s in dados_tratados]
        else:
            dados_tratados = [int(s) if s.isdigit() else -1 if s == 'None' else s for s in dados_tratados]
        return dados_tratados
    
    def tratamentoAtuadores(self,dados):
        servo="Nenhum servo"
        sentido="Centro"
        if dados[0] and dados[2] == 20:
            servo = "Vertical"
            sentido="Norte"
        elif dados[0] and dados[2] == -20:
            servo = "Vertical"
            sentido="Sul"
        elif dados[1] and dados[2] == 20:
            servo = "Horizontal"
            sentido="Leste"
        elif dados[1] and dados[2] == -20:
            servo = "Horizontal"
            sentido="Oeste"    
        return(f"{servo} se encontra direcionado. Sentido atual: {sentido}") 
        
    def dadosSensor(self, dados):
        try:
            dados_tratados = self.tratamento(dados)
            conf = json.loads(self.conf)
            sensor1= 0
            sensor2=0
            angulo=0
            valor_atual=-1
            for i, valor in enumerate(dados_tratados):
                if valor> conf["valorMin"] > valor_atual:
                    valor_atual=valor
                    if (i == 0 and conf["sensorNorte"] == 1 and conf["atuaVert"] == 1):
                        angulo = 20
                        sensor1 = 1
                        sensor2 = 0
                    elif (i == 1 and conf["sensorSul"] == 1 and conf["atuaVert"] == 1):
                        angulo = -20
                        sensor1 = 1
                        sensor2 = 0
                    elif (i == 2 and conf["sensorLeste"] == 1 and conf["atuaHoriz"] == 1):
                        angulo = 20
                        sensor1 = 0
                        sensor2 = 1
                    elif (i == 3 and conf["sensorOeste"] == 1 and conf["atuaHoriz"] == 1):
                        angulo = -20
                        sensor1 = 0
                        sensor2 = 1
                    break
            
                     
            
            sensor = {
                "Leste": float(dados_tratados[2]),
                "Norte": float(dados_tratados[0]),
                "Oeste": float(dados_tratados[3]),
                "Sul": float(dados_tratados[1])
            }
            mapeamento_booleano = {1: True, 0: False}
            atuadores = {
                "angulo": angulo,
                "sensor1": mapeamento_booleano[sensor1],
                "sensor2": mapeamento_booleano[sensor2]
            }
            sensor_json = json.dumps(sensor)
            atuadores_json = json.dumps(atuadores)
            return [sensor_json, atuadores_json]
        except Exception as e:
            return f"Erro na função sensores: {str(e)}"
        