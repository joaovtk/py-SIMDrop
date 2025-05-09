import logging
import paypalrestsdk
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import dotenv_values, load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()
PAYPAL_CLIENT_ID =  os.getenv("CLIENT_ID")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET")

# Token do bot do Telegram
TOKEN = os.getenv("TOKEN")

# Credenciais do PayPal

# Dicionário para armazenar o saldo dos usuários (por ID)
user_balances = {}

# Habilitar o log para depuração
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar o PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # ou "live" para produção
    "client_id": PAYPAL_CLIENT_ID,
    "client_secret": PAYPAL_SECRET
})

# Função para consultar saldo do usuário
async def check_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    balance = user_balances.get(user_id, 0)
    await update.message.reply_text(f"Seu saldo é: R${balance},00")

# Função para gerar o link de pagamento via PayPal
async def generate_payment_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "transactions": [{
            "amount": {"total": "10.00", "currency": "BRL"},
            "description": "Recarregar saldo no bot"
        }],
        "redirect_urls": {
            "return_url": "http://localhost:5000/payment-success",
            "cancel_url": "http://localhost:5000/payment-cancel"
        }
    })

    if payment.create():
        approval_url = next(link.href for link in payment.links if link.rel == "approval_url")
        await update.message.reply_text(f"Por favor, efetue o pagamento clicando no link abaixo:\n{approval_url}")
    else:
        await update.message.reply_text("Erro ao criar o pagamento, tente novamente.")

# Função para gerar número virtual (simulado)
async def buy_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    balance = user_balances.get(user_id, 0)

    if balance < 10:
        await update.message.reply_text("Você não tem saldo suficiente para comprar um número virtual. Recarregue seu saldo.")
        return

    user_balances[user_id] -= 10
    await update.message.reply_text(f"Seu número virtual foi gerado: +1 234 567 890")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    "Comandos disponíveis:\n"
    "/ajuda - Mostra esta lista de comandos\n"
    "/start - Inicia o bot\n"
    "/saldo - Ver seu saldo\n"
    "/recarregar - Recarregar saldo\n"
    "/comprar - Comprar número"
)


# Função de comando "/start"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bem-vindo! Use /comprar para obter um número virtual. Seu saldo será descontado.")

# Função principal que configura o bot
def telegram_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("comprar", buy_number))
    application.add_handler(CommandHandler("saldo", check_balance))
    application.add_handler(CommandHandler("recarregar", generate_payment_link))
    application.add_handler(CommandHandler("ajuda", help))

    application.run_polling()
