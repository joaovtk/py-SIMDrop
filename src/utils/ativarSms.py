from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext

from utils.database import con, cursor
from config import *
import requests

async def ativar_sms(orderid):
    url_ativacao = f"{URL_SMS_ACTIVATE_API}/activation/sms/{orderid}"
    header = {
        "apikey": API_SMS_ACTIVATE_KEY
    }

    try:
        response = requests.get(url_ativacao, headers=header, timeout=10)
        response.raise_for_status()  # Levanta erro se o status não for 200
        resultado = response.json()

        if 'error' in resultado:
            raise ValueError(f"Erro na ativação do SMS: {resultado['error']}")

        # Retorna sucesso e mensagem de ativação
        return True, resultado["code"]
    except requests.exceptions.RequestException as e:
        return False, str(e)