from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext

from utils.database import con, cursor
from config import *
import requests
import time
from handlers.start import start
import datetime

async def gerar_qrcode_pix(pedido_id, update: Update):
    url = "https://api.abacatepay.com/v1/billing/create"  # URL fictícia de exemplo
    cpf = con.execute(f"SELECT cpf FROM user WHERE userid = {update.effective_user.id}")
    cpf = cpf.fetchone()
    # Ajustando o payload com os valores dinâmicos
    payload = {
        "frequency": "ONE_TIME",
        "methods": ["PIX"],
        "products": [
            {
                "externalId": f"1prod",  # Usando o pedido_id para gerar um ID único
                "name": "Compra de numero",
                "description": "Compra de Numero",
                "quantity": 1,
                "price": 500 # Usando o valor total calculado
            }
        ],
        "returnUrl": "https://web.telegram.org/a/#8059941460",
        "completionUrl": "https://web.telegram.org/a/#8059941460",
        "customer": {
            "name": str(update.effective_user.id),
            "cellphone": "00000000000",
            "email": "exemplo@gmail.com",
            "taxId": cpf
        }
    }

    headers = {
        "Authorization": f"Bearer {ABACATE_TOKEN}",  # novo token no .env
        "Content-Type": "application/json"
    }


    response = requests.post(url, json=payload, headers=headers)

    data = response.json()["data"]
    
    print(response.status_code)

    return data["url"]

