from flask import Flask, request
from utils.database import con, cursor
from config import TOKEN_TELEGRAM
import requests

app = Flask(__name__)

def atualizar_saldo(userid, valor):
    cursor.execute("SELECT saldo FROM usuarios WHERE userid = ?", (userid,))
    row = cursor.fetchone()
    if row:
        novo_saldo = row[0] + float(valor)
        cursor.execute("UPDATE usuarios SET saldo = ? WHERE userid = ?", (novo_saldo, userid))
    else:
        cursor.execute("INSERT INTO usuarios (userid, saldo) VALUES (?, ?)", (userid, valor))
    con.commit()

def get_chat_id(userid):
    cursor.execute("SELECT chat_id FROM usuarios WHERE userid = ?", (userid,))
    row = cursor.fetchone()
    return row[0] if row else None

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)

@app.route('/webhook/pixup', methods=['POST'])
def pixup_webhook():
    data = request.json
    print("📥 Webhook recebido:", data)

    if data.get("status") == "approved":
        valor = float(data.get("amount"))
        userid = data.get("custom_id")
        atualizar_saldo(userid, valor)
        chat_id = get_chat_id(userid)
        if chat_id:
            send_telegram_message(chat_id, f"✅ Pagamento de R${valor:.2f} confirmado! Seu saldo foi atualizado.")
        else:
            print(f"⚠️ Usuário com userid {userid} não encontrado no banco.")
    return '', 200

@app.route("/test", methods=["GET"])
def test():
    return "Test"

def run_webhook():
    app.run(host='0.0.0.0', port=5000)
