from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from utils.database import cursor, con

async def debug_add_saldo(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    args = context.args

    if not args:
        await update.message.reply_text("Uso: /debugsaldo <valor>")
        return

    try:
        valor = float(args[0])
    except ValueError:
        await update.message.reply_text("O valor precisa ser numérico.")
        return

    user = get_user_by_telegram_id(user_id)
    if not user:
        await update.message.reply_text("Usuário não encontrado no banco de dados.")
        return

    add_saldo(user_id, valor)
    if update.message:
        await update.message.reply_text(f"✅ Saldo de R${valor:.2f} adicionado com sucesso (DEBUG).")
    else:
        await update.callback_query.edit_message_text(f"✅ Saldo de R${valor:.2f} adicionado com sucesso (DEBUG).")

def add_saldo(telegram_id, valor):
    cursor.execute("UPDATE user SET saldo = saldo + ? WHERE userid = ?", (valor, telegram_id))
    con.commit()
    con.close()

def get_user_by_telegram_id(telegram_id):
    cursor.execute("SELECT * FROM user WHERE userid = ?", (telegram_id,))
    user = cursor.fetchone()
    con.close()
    return user