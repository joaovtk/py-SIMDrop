from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext

from utils.database import con, cursor
from utils.gerar_qr import gerar_qrcode_pix
from config import *
import requests
import time
from handlers.start import start
import datetime
async def comprar(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    pedido_id_seq = 1

    # 🔎 Buscar service e pais do banco de dados
    cursor.execute("SELECT service, pais FROM user WHERE userid = ?", (user_id,))
    dados = cursor.fetchone()

    if not dados:
        await update.message.reply_text("❌ Usuário não encontrado. Use /start para se registrar.")
        return

    service, pais = dados

    # Verificações se os dados foram preenchidos
    if not service or service.lower() == "none":
        if update.message:
            await update.message.reply_text("⚠️ Você precisa escolher um serviço primeiro.\nUse o botão '📱 Escolher serviço'.")
            time.sleep(3.5)
            await start(update, context)
        else:
            await update.callback_query.edit_message_text("⚠️ Você precisa escolher um serviço primeiro.\nUse o botão '📱 Escolher serviço'.")
            time.sleep(3.5)
            await start(update, context)
        return

    if not pais or pais.lower() == "none":
        if update.message:
            await update.message.reply_text("⚠️ Você precisa escolher um país primeiro.\nUse o botão '🌍 Escolher país'.")
            time.sleep(3.5)
            await start(update, context)
        else:
            await update.callback_query.edit_message_text("⚠️ Você precisa escolher um país primeiro.\nUse o botão '🌍 Escolher país'.")
            time.sleep(3.5)
            await start(update, context)
        return

    pais = pais.upper()
    header = { "apikey": API_SMS_ACTIVATE_KEY }


    # Consulta os preços de serviço com base no país e serviço
    response = requests.get(f"{URL_SMS_ACTIVATE_API}/servicesprices", headers=header, timeout=10)
    response.raise_for_status()
    data = response.json().get('data', [])

    # Encontrar o serviço específico e preço
    servico_info = next((s for s in data if s['service'] == service and s['country'] == pais), None)
    if not servico_info:
        if update.message:
            await update.message.reply_text(f"❌ Serviço '{service}' não está disponível no país '{pais}'.")
        else:
            await update.callback_query.edit_message_text(f"❌ Serviço '{service}' não está disponível no país '{pais}'.")
        return

    preco_unitario = float(servico_info['price'])


    # Preço total e quantidade
    preco_total = round((preco_unitario + 1) * 1, 2)  # Exemplo de 1 unidade
    pedido_id = pedido_id_seq
    pedido_id_seq += 1

    pedidos[pedido_id] = {
        "user_id": user_id,
        "quantidade": 1,  # Exemplo de uma quantidade fixa
        "preco_unitario": preco_unitario,
        "preco_total": preco_total,
        "status": "pendente",
        "timestamp": datetime.datetime.now(),
        "mp_preferencia_url": None,
        "mp_pagamento_id": None,
        "sms_compra_result": None,
        "servico_opcao": service,
        "pais": pais
    }
    cursor.execute("SELECT service, pais FROM user WHERE userid = ?", (user_id,))
    dados = cursor.fetchone()

    if not dados:
        await update.message.reply_text("❌ Usuário não encontrado. Use /start para se registrar.")
        return

    service, pais = dados



    qrcode_url = await gerar_qrcode_pix(pedido_id, update)
    if qrcode_url == "None":
        time.sleep(5)
        await start(update, context)
    else:
        pedidos[pedido_id]["mp_preferencia_url"] = qrcode_url

        # Enviar confirmação ao usuário
        if update.message:
            await update.message.reply_text(
            f"🧾 Pedido {pedido_id} criado com sucesso!\n\n"
            f"📱 Serviço: {servico_info['serviceDescription']}\n"
            f"🌍 País: {pais}\n"
            f"🔢 Quantidade: 1\n"  # Exemplo de 1 unidade
            f"💰 Total: ${preco_total:.2f}\n\n"
            f"✅ Para pagar, escaneie o QR Code PIX ou clique no link abaixo:\n\nℹ️ Lembre-se de inserir telefone e email no link\n\n{qrcode_url}",
        )
            
        else:
            await update.callback_query.edit_message_text(
            f"🧾 Pedido {pedido_id} criado com sucesso!\n\n"
            f"📱 Serviço: {servico_info['serviceDescription']}\n"
            f"🌍 País: {pais}\n"
            f"💵 Preço Unitário: ${preco_unitario:.2f}\n"
            f"🔢 Quantidade: 1\n"  # Exemplo de 1 unidade
            f"💰 Total: ${preco_total:.2f}\n\n"
            f"✅ Para pagar, escaneie o QR Code PIX ou clique no link abaixo:\n{qrcode_url}",

        )

