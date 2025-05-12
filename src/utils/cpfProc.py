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
    
    mensagem_boas_vindas = (
        f"👋 Olá novamente, {update.effective_user.first_name}!\n\n"
        "🫂 Seu cadastro já está ativo no sistema.\n\n"
        "Use os botões abaixo para navegar pelas opções disponíveis. Aqui está uma breve explicação de cada função:\n\n"
        "📱 `Escolher Serviço` — Selecione um serviço como *Google*, *WhatsApp*, entre outros.\n\n"
        "🌍 `Escolher País` — Escolha o país de origem do número, como *Brasil* ou *Estados Unidos*.\n\n"
        "🔃 `*Fazer Recarga de Saldo*` — Adicione créditos à sua conta para comprar números.\n\n"
        "✅ `Checar Números` — Verifique os números comprados e armazenados no banco de dados.\n\n"
        "📣 `Comprar Número` — Adquira um número virtual disponível pela API da SMS-PVA.\n\n"
    )

    await update.callback_query.edit_message_text(
            mensagem_boas_vindas,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("📱 Escolher serviço", callback_data="serv"),
                    InlineKeyboardButton("🌍 Escolher país", callback_data="pais")
                ],
                [
                    InlineKeyboardButton("💰 Ver saldo", callback_data="saldo"),
                    InlineKeyboardButton("🔃 Fazer Recarga de Saldo", callback_data="recarregar")
                ],
                [
                    InlineKeyboardButton("📣 Comprar Número", callback_data="sms"),
                    InlineKeyboardButton("✅ Checar Números", callback_data="ativar")
                ],

                [
                    InlineKeyboardButton("ℹ️ Ajuda", callback_data="ajuda"),
                    InlineKeyboardButton("❔ Duvidas ", callback_data="duvidas")
                ]
        ])
    )

    return CONCLUIDO

