from telegram.ext import ConversationHandler, CallbackContext
from telegram import Update
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("⚠️ O processo foi cancelado.")
    return ConversationHandler.END

