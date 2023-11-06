import json


class Validadores:
    @staticmethod
    def configuracoes(dados):
        campos_esperados = [
            'valorMin',
            'sensorNorte',
            'sensorSul',
            'sensorLeste',
            'sensorOeste',
            'atuaHoriz',
            'atuaVert'
        ]

        if not all(campo in dados for campo in campos_esperados):
            raise ValueError("Campos ausentes no JSON")

        tipos_esperados = {
            'valorMin': float,
            'sensorNorte': bool,
            'sensorSul': bool,
            'sensorLeste': bool,
            'sensorOeste': bool,
            'atuaHoriz': bool,
            'atuaVert': bool
        }

        for campo, tipo in tipos_esperados.items():
            if not isinstance(dados[campo], tipo):
                raise ValueError(f"O campo '{campo}' deve ser do tipo {tipo.__name__}")

        return True
    @staticmethod
    def sensores(dados):
        campos_esperados = [
            'Norte',
            'Sul',
            'Leste',
            'Oeste'
        ]

        if not all(campo in dados for campo in campos_esperados):
            raise ValueError("Campos ausentes no JSON")

        tipos_esperados = {
            'Norte': float,
            'Sul': float,
            'Leste': float,
            'Oeste': float
        }

        for campo, tipo in tipos_esperados.items():
            if not isinstance(dados[campo], tipo):
                raise ValueError(f"O campo '{campo}' deve ser do tipo {tipo.__name__}")
        
        return True
    @staticmethod
    def atuadores(dados):
        campos_esperados = [
            'sensor1',
            'sensor2',
            'angulo'
        ]

        if not all(campo in dados for campo in campos_esperados):
            raise ValueError("Campos ausentes no JSON")

        tipos_esperados = {
            'sensor1': bool,
            'sensor2': bool,
            'angulo': int
        }

        for campo, tipo in tipos_esperados.items():
            if not isinstance(dados[campo], tipo):
                raise ValueError(f"O campo '{campo}' deve ser do tipo {tipo.__name__}")

        if 'angulo' in dados and dados['angulo'] not in [-20, 0, 20]:
            raise ValueError("O campo 'angulo' deve ser um número inteiro e deve estar entre -20, 0 ou 20.")

        return True