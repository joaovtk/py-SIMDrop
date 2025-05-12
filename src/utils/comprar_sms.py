
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext

from utils.database import con, cursor
from utils.ativarSms import ativar_sms
from config import *
import requests
from utils.log import logger


async def comprar_sms_sms_pva(service_id, quantidade, pais, update: Update):
    params = {
        "service": service_id,  # Usando o ID do serviço
        "country": pais,   # código do país
    }

    header = {
        "apikey": API_SMS_ACTIVATE_KEY,
        "Content-length": "2"
    }

    url = f"{URL_SMS_ACTIVATE_API}/number/{params['country']}/{params['service']}"

    try:
        print(params)
        r = requests.get(url, headers=header)
        resultado = r.json()

        if 'error' in resultado:
            raise ValueError(f"Erro na API SMS-PVA: {resultado['error']}")

        # Obter o número e orderid
        numero = resultado['data']["phoneNumber"]
        orderid = resultado['data']["orderId"]
        
        # Ativando o SMS com o orderid
        if update.message:
            await update.message.reply_text("🚀 Validando seu número... já já ele é seu!")

        else:
            await update.message.reply_text("🚀 Validando seu número... já já ele é seu!")
        sucesso, code = await ativar_sms(orderid)
        
        if sucesso:
            # Retorna o sucesso da ativação junto com o número e a mensagem
            return {"status": True, "number": numero, "code": code}
        else:
            # Retorna erro caso a ativação falhe
            return {}

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na API SMS-PVA: {e}")
        return {}