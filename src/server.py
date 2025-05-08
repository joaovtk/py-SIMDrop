import paypalrestsdk
from flask import Flask, request, jsonify
from dotenv import dotenv_values

# Carregar variáveis de ambiente
env = dotenv_values(".env")

# Credenciais do PayPal
PAYPAL_CLIENT_ID = env['CLIENT_ID']
PAYPAL_SECRET = env['PAYPAL_SECRET']

# Inicializar o PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # ou "live" para produção
    "client_id": PAYPAL_CLIENT_ID,
    "client_secret": PAYPAL_SECRET
})

# URL do webhook (para confirmar o pagamento)
PAYPAL_WEBHOOK_URL = env['PAYPAL_WEBHOOK_URL']

# Dicionário para armazenar o saldo dos usuários (por ID)
user_balances = {}

# Configuração do Flask
app = Flask(__name__)

# Função para processar o pagamento após sucesso
@app.route('/payment-success', methods=['POST'])
def payment_success():
    data = request.json
    payment_id = data.get('payment_id')
    payer_id = data.get('payer_id')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.state == "approved":
        user_id = payer_id  # Usando payer_id como ID do usuário
        user_balances[user_id] = user_balances.get(user_id, 0) + 10  # Adiciona R$10 ao saldo do usuário
        return jsonify({'status': 'Pagamento bem-sucedido', 'balance': user_balances[user_id]})

    return jsonify({'status': 'Erro ao processar pagamento'}), 400

# Função para processar o cancelamento do pagamento
@app.route('/payment-cancel', methods=['GET'])
def payment_cancel():
    return jsonify({'status': 'Pagamento cancelado, tente novamente mais tarde'}), 400

# Função para rodar o Flask
def flask_app():
    app.run(port=5000)
