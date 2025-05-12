from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import time
from handlers.start import start

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👟 Voltar ao menu Start", callback_data="exit")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("📞 Fale comigo no contatos abaixo: \n\nDiscord: `GoiabaTk`\n\nTelegram: `+55 31 99216 9431`\n\nGithub: `joaovtk`\n\n\n", parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    else:
        await update.callback_query.edit_message_text("📞 Fale comigo no contatos abaixo: \n\nDiscord: `GoiabaTk`\n\nTelegram: `+55 31 99216 9431`\n\nGithub: `joaovtk`\n\n\n", parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    
