from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, ContextTypes, CallbackQueryHandler
from telegram.ext import MessageHandler, filters, ConversationHandler
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from config import *
from utils.cancel import cancel
from utils.cpfProc import processar_cpf
from handlers.buttonhandler import button_handler
from handlers.debug import debug_add_saldo
from handlers.start import start
from handlers.ajuda import ajuda


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()

    # Definir a conversa
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PEDIR_CPF: [MessageHandler(filters.TEXT & ~filters.COMMAND, processar_cpf)],
            CONCLUIDO: [MessageHandler(filters.ALL, cancel)],  # ou qualquer lógica que queira após o CPF
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("ajuda", ajuda))

    if STATUS == "DEV":
        app.add_handler(CommandHandler("debugsaldo", debug_add_saldo))

    # Registrar o handler de conversa
    app.add_handler(conv_handler)

    # Rodar o bot
    print("Bot iniciado")
    app.run_polling()