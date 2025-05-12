from dotenv import dotenv_values, load_dotenv
import os
STATUS = "DEV"
if STATUS != "DEV":
    load_dotenv()
    TOKEN_TELEGRAM = os.getenv("TOKEN")
    API_SMS_ACTIVATE_KEY = os.getenv("SMS_API_KEY")
    URL_SMS_ACTIVATE_API = os.getenv("SMS_API_URL")
    ABACATE_TOKEN = os.getenv("ABACATE_TOKEN")
else:
    env = dotenv_values(".env")
    TOKEN_TELEGRAM = env["TOKEN"]
    API_SMS_ACTIVATE_KEY = env["SMS_API_KEY"]
    URL_SMS_ACTIVATE_API = env["SMS_API_URL"]
    ABACATE_TOKEN = env["ABACATE_TOKEN"]
PEDIR_CPF = 1
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