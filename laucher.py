import threading
from src.main import telegram_bot
from src.server import flask_app
from src.ping import send_ping

# Função para rodar ambos no mesmo processo
def main():
    send_ping()
    # Rodando Flask em um thread separado
    flask_thread = threading.Thread(target=flask_app)
    flask_thread.start()

    # Rodando o Telegram bot no processo principal
    telegram_bot()

if __name__ == '__main__':
    main()
