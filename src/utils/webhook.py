from flask import Flask, request
import requests
from utils.database import con, cursor  # sua conexão global
from config import *
app = Flask(__name__)


def atualizar_saldo(userid, valor):
    cursor.execute("SELECT saldo FROM usuarios WHERE userid = ?", (userid,))
    row = cursor.fetchone()

    if row:
        saldo_atual = row[0]
        novo_saldo = saldo_atual + float(valor)
        cursor.execute("UPDATE usuarios SET saldo = ? WHERE userid = ?", (novo_saldo, userid))
    else:
        # Se o usuário não existir, pode-se registrar aqui (se desejar)
        cursor.execute("INSERT INTO usuarios (userid, saldo) VALUES (?, ?)", (userid, valor))

    con.commit()

def get_chat_id(userid):
    cursor.execute("SELECT chat_id FROM usuarios WHERE userid = ?", (userid,))
    row = cursor.fetchone()
    return row[0] if row else None

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(url, data=payload)

@app.route('/webhook/pixup', methods=['POST'])
def pixup_webhook():
    data = request.json
    print("Webhook recebido:", data)

    if data.get("status") == "approved":
        valor = float(data.get("amount"))
        userid = data.get("custom_id")  # Esse é o seu 'userid' no banco

        atualizar_saldo(userid, valor)
        chat_id = get_chat_id(userid)

        if chat_id:
            send_telegram_message(chat_id, f"✅ Pagamento de R${valor:.2f} confirmado! Seu saldo foi atualizado.")
        else:
            print(f"⚠️ Usuário com userid {userid} não encontrado no banco.")

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)
