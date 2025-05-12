from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext

from utils.database import con, cursor
from config import *

async def processar_cpf(update: Update, context: CallbackContext):
    cpf = update.message.text.strip()

    # Validação do CPF (adapte conforme necessário)
    if len(cpf) != 11 or not cpf.isdigit():
        await update.message.reply_text("❌ CPF inválido. Por favor, insira um CPF válido (somente números).")
        return PEDIR_CPF  # Retorna ao estado de pedido de CPF

    # Armazena o CPF no banco de dados
    cursor.execute("UPDATE user SET cpf = ? WHERE userid = ?", (cpf, update.effective_user.id))
    con.commit()

    # Envia uma única vez a mensagem de sucesso com o botão de escolha
    await update.message.reply_text(
        "✅ CPF registrado com sucesso! Agora, escolha um serviço para comprar números virtuais.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📱 Escolher serviço", callback_data="serv")],
            [InlineKeyboardButton("🌍 Escolher país", callback_data="pais")],
            [InlineKeyboardButton("💰 Ver saldo", callback_data="saldo")],
            [InlineKeyboardButton("🔃 Recarregar", callback_data="recarregar")],
        ])
    )

    return CONCLUIDO

