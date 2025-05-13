from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext

from utils.database import con, cursor
from config import *
import requests
import time
from handlers.start import start
import datetime

async def gerar_qrcode_pix(pedido_id, update: Update):
    url = "https://api.pixupbr.com/v2/pix/qrcode"  # URL fictícia de exemplo
    # Ajustando o payload com os valores dinâmicos
    payload = {
        "amount": 1,    
        "payer": {
            "name": update.effective_user.name
        },
        "postbackUrl": "http://localhost:5000/webhook/pixup"
    }

    headers = {
        "Authorization": f"Bearer {PIX_UP}",  # novo token no .env
        "Content-Type": "application/json"
    }


    response = requests.post(url, json=payload, headers=headers)

    data = response.json()
    if data["statusCode"] == 401:
        await update.callback_query.edit_message_text("⚠️ Ocorreu um erro ao processar o pagamento via Pix. Por favor, tente novamente mais tarde. Redirecionando para /start em 10 segundos")
        return "None"
    else:
        return data["qrcode"]

