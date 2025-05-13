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
            saldo FLOAT DEFAULT 0.0
        )
    """)

    saldo = cursor.execute(f"SELECT saldo FROM user WHERE userid = {update.effective_user.id}")
    saldo = saldo.fetchone()

    if not saldo:
        saldo = 0
    else:
        saldo = saldo[0]
    mensagem_boas_vindas = f"👋 Olá novamente, {update.effective_user.first_name}!\n\n🫂 Seu cadastro já está ativo no sistema.\n\nUse os botões abaixo para navegar pelas opções disponíveis. Aqui está uma breve explicação de cada função:\n\n`Escolher Serviço` — Selecione um serviço como *Google*, *WhatsApp*, entre outros.\n\n `Escolher País` — Escolha o país de origem do número, como *Brasil* ou *Estados Unidos*.\n\n`Fazer Recarga de Saldo` — Adicione créditos à sua conta para comprar números.\n\n`Checar Números` — Verifique os números comprados e armazenados no banco de dados.\n\n`Comprar Número` — Adquira um número virtual disponível pela API da SMS-PVA.\n\n`Ajuda/FAQ` — Consiga ajuda com nosso canais de comunicação\n\n`Duvidas` — Aqui tem todas as possiveis perguntas\n\n`Aba de Favoritos` — Lá estarão presentes os países e serviços que você salvou\n\n\nSeu Saldo é de: ${saldo} BRL\n\n"
    if update.message:
        message_id = update.message.id
    else:
        message_id = update.callback_query.message.id
    context.user_data["msg_user_id"] = message_id

    if update.message:
        await update.message.reply_text(
        mensagem_boas_vindas,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📱 Escolher Serviço", callback_data="serv")
            ],
            [
                InlineKeyboardButton("🏁 Escolher País", callback_data="pais")
            ],
            [
                InlineKeyboardButton("🏦 Saldo", callback_data="saldo"),
                InlineKeyboardButton("🔃 Fazer Recarga de Saldo", callback_data="recarregar")
            ],
            [
                InlineKeyboardButton("💸 Comprar Número", callback_data="sms"),
                InlineKeyboardButton("☎️ Checar Números", callback_data="ativar")
            ],

            [
                InlineKeyboardButton("❔ Ajuda/FAQ", callback_data="ajuda"),
                InlineKeyboardButton("❗ Duvidas ", callback_data="duvidas")
            ],
            [
                InlineKeyboardButton("🌟 Aba de Paises Favoritos", callback_data="favorito_pais"),
                InlineKeyboardButton("⭐ Aba de Serviços Favoritos", callback_data="favorito_serv")
            ],
            [
                InlineKeyboardButton("🗑️ Apagar", callback_data="erase")
            ],

        ]),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.callback_query.edit_message_text(
        mensagem_boas_vindas,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📱 Escolher Serviço", callback_data="serv")
            ],
            [
                InlineKeyboardButton("🏁 Escolher País", callback_data="pais")
            ],
            [
                InlineKeyboardButton("🏦 Saldo", callback_data="saldo"),
                InlineKeyboardButton("🔃 Fazer Recarga de Saldo", callback_data="recarregar")
            ],
            [
                InlineKeyboardButton("💸 Comprar Número", callback_data="sms"),
                InlineKeyboardButton("☎️ Checar Números", callback_data="ativar")
            ],

            [
                InlineKeyboardButton("❔ Ajuda/FAQ", callback_data="ajuda"),
                InlineKeyboardButton("❗ Duvidas ", callback_data="duvidas")
            ],
            [
                InlineKeyboardButton("🌟 Aba de Paises Favoritos", callback_data="favorito_pais"),
                InlineKeyboardButton("⭐ Aba de Serviços Favoritos", callback_data="favorito_serv")
            ],
            [
                InlineKeyboardButton("🗑️ Apagar", callback_data="erase")
            ],

        ]),
            parse_mode=ParseMode.MARKDOWN
        )

   

    return ConversationHandler.END
