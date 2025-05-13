from dotenv import dotenv_values, load_dotenv
import os
STATUS = "PROD"
if STATUS != "DEV":
    load_dotenv()
    STATUS = os.getenv("STATUS")
    TOKEN_TELEGRAM = os.getenv("TOKEN")
    API_SMS_ACTIVATE_KEY = os.getenv("SMS_API_KEY")
    URL_SMS_ACTIVATE_API = os.getenv("SMS_API_URL")
    PIX_UP = os.getenv("ABACATE_TOKEN")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
else:
    env = dotenv_values(".env")
    STATUS = env["STATUS"]
    TOKEN_TELEGRAM = env["TOKEN"]
    API_SMS_ACTIVATE_KEY = env["SMS_API_KEY"]
    URL_SMS_ACTIVATE_API = env["SMS_API_URL"]
    PIX_UP = env["ABACATE_TOKEN"]
    HOST = env["HOST"]
    PORT = env["PORT"]
CONCLUIDO = 2
PAISES_VALIDOS = {
    "BR": "Brasil",
    "US": "Estados Unidos",
    "RU": "Rússia",
    "IN": "Índia",
    "DE": "Alemanha",
    "FR": "França",
    "IT": "Itália",
    "GB": "Reino Unido",
    "CA": "Canadá",
    "ES": "Espanha",
    "AU": "Austrália",
    "MX": "México",
    "JP": "Japão",
    "ZA": "África do Sul",
    "KR": "Coreia do Sul",
    "AR": "Argentina",
    "CN": "China",
    "NG": "Nigéria",
    "EG": "Egito",
    "PL": "Polônia",
    "ID": "Indonésia"
}

pedidos = {}