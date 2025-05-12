from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters
from config import TOKEN_TELEGRAM, STATUS
from handlers.start import start
from handlers.ajuda import ajuda
from handlers.buttonhandler import button_handler
from handlers.debug import debug_add_saldo
from handlers.drop import drop
from utils.cpfProc import processar_cpf
from utils.cancel import cancel

# Constantes dos estados
from config import PEDIR_CPF, CONCLUIDO

def run_bot():
    app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PEDIR_CPF: [MessageHandler(filters.TEXT & ~filters.COMMAND, processar_cpf)],
            CONCLUIDO: [MessageHandler(filters.ALL, cancel)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CallbackQueryHandler(button_handler))

    if STATUS == "DEV":
        app.add_handler(CommandHandler("debugsaldo", debug_add_saldo))
        app.add_handler(CommandHandler("drop", drop))

    app.add_handler(conv_handler)

    app.run_polling()
