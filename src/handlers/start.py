from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from utils.database import con, cursor
from config import *

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            userid INTEGER PRIMARY KEY,
            service TEXT DEFAULT 'None',
            pais TEXT DEFAULT 'None',
            saldo FLOAT DEFAULT 0.0,
            cpf TEXT DEFAULT 'None'
        )
    """)
    con.commit()

    user_id = update.effective_user.id
    cursor.execute(f"SELECT * FROM user WHERE userid = {user_id}")
    user_exists = cursor.fetchone()

    if not user_exists:
        cursor.execute(
            "INSERT INTO user (userid) VALUES (?)",
            (user_id,)
        )
        con.commit()

        await update.message.reply_text(
            f"👋 Olá, {update.effective_user.first_name}!\n\n"
            "Seja bem-vindo ao nosso bot!\n\n"
            "Para começarmos, por favor, informe seu *CPF* (somente os números).",
            parse_mode=ParseMode.MARKDOWN
        )
        return PEDIR_CPF

    saldo = cursor.execute("SELECT saldo FROM user WHERE userid = ?", (user_id,))
    saldo = saldo.fetchone()

    mensagem_boas_vindas = f"👋 Olá novamente, {update.effective_user.first_name}!\n\n🫂 Seu cadastro já está ativo no sistema.\n\nUse os botões abaixo para navegar pelas opções disponíveis. Aqui está uma breve explicação de cada função:\n\n📱 `Escolher Serviço` — Selecione um serviço como *Google*, *WhatsApp*, entre outros.\n\n 🌍 `Escolher País` — Escolha o país de origem do número, como *Brasil* ou *Estados Unidos*.\n\n🔃 `Fazer Recarga de Saldo` — Adicione créditos à sua conta para comprar números.\n\n✅ `Checar Números` — Verifique os números comprados e armazenados no banco de dados.\n\n 📣 `Comprar Número` — Adquira um número virtual disponível pela API da SMS-PVA.\n\n"
    

    if update.message:
        await update.message.reply_text(
        mensagem_boas_vindas,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Escolher Serviço", callback_data="serv"),
                InlineKeyboardButton("Escolher País", callback_data="pais")
            ],
            [
                InlineKeyboardButton("Ver Saldo", callback_data="saldo"),
                InlineKeyboardButton("Fazer Recarga de Saldo", callback_data="recarregar")
            ],
            [
                InlineKeyboardButton("Comprar Número", callback_data="sms"),
                InlineKeyboardButton("Checar Números", callback_data="ativar")
            ],

            [
                InlineKeyboardButton("Ajuda/FAQ", callback_data="ajuda"),
                InlineKeyboardButton("Duvidas ", callback_data="duvidas")
            ]
        ]),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.callback_query.edit_message_text(
        mensagem_boas_vindas,
        reply_markup=InlineKeyboardMarkup([
             [
                InlineKeyboardButton("Escolher Serviço", callback_data="serv"),
                InlineKeyboardButton("Escolher País", callback_data="pais")
            ],
            [
                InlineKeyboardButton("Ver Saldo", callback_data="saldo"),
                InlineKeyboardButton("Fazer Recarga de Saldo", callback_data="recarregar")
            ],
            [
                InlineKeyboardButton("Comprar Número", callback_data="sms"),
                InlineKeyboardButton("Checar Números", callback_data="ativar")
            ],

            [
                InlineKeyboardButton("Ajuda/FAQ", callback_data="ajuda"),
                InlineKeyboardButton("Duvidas ", callback_data="duvidas")
            ]
        ]),
        parse_mode=ParseMode.MARKDOWN
    )
        

    return ConversationHandler.END
