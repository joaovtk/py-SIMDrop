from telegram import  Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import time
from handlers.start import start

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("📞 Fale comigo no contatos abaixo: \n\nDiscord: `GoiabaTk`\n\nTelegram: `+55 31 99216 9431`\n\nGithub: `joaovtk`\n\n\nRedirecionando para /start em 10 segundos", parse_mode=ParseMode.MARKDOWN)
    else:
        await update.callback_query.edit_message_text("📞 Fale comigo no contatos abaixo: \n\nDiscord: `GoiabaTk`\n\nTelegram: `+55 31 99216 9431`\n\nGithub: `joaovtk`\n\n\nRedirecionando para /start em 10 segundos", parse_mode=ParseMode.MARKDOWN)

    time.sleep(10)

    await start(update, context)
