
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext

from utils.database import con, cursor
from config import *
import requests
async def verificar_pagamento(update: Update, context: CallbackContext):
    if len(context.args) != 1 or not context.args[0].isdigit():
        await update.message.reply_text("❌ Use o comando corretamente: /verificar_pagamento <id_do_pedido>")
        return

    pedido_id = int(context.args[0])

    if pedido_id not in pedidos:
        await update.message.reply_text("❌ Pedido não encontrado.")
        return

    pedido = pedidos[pedido_id]
    if pedido["status"] == "concluido":
        await update.message.reply_text("✅ Este pedido já foi concluído.")
        return

    # Verificar pagamento com Abacate Pay
    url = f"https://api.abacatepay.com/v1/billing/details?externalId=1prod"
    headers = {
        "Authorization": f"Bearer {ABACATE_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        await update.message.reply_text("⚠️ Erro ao verificar o pagamento. Tente novamente mais tarde.")
        return

    data = response.json()["data"]
    status = data.get("status")

    if status == "COMPLETED":
        user_id = pedido["user_id"]
        valor = pedido["preco_total"]
        cursor.execute("UPDATE user SET saldo = saldo + ? WHERE userid = ?", (valor, user_id))
        con.commit()
        pedidos[pedido_id]["status"] = "concluido"

        await update.message.reply_text(f"💵 Pagamento confirmado! Saldo atualizado com +${valor:.2f}.")
    else:
        await update.message.reply_text(f"⏳ O pagamento ainda não foi confirmado. Status atual: {status}")