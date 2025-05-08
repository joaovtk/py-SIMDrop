import threading
from main import telegram_bot
from server import flask_app

# Função para rodar ambos no mesmo processo
def main():
    # Rodando Flask em um thread separado
    flask_thread = threading.Thread(target=flask_app)
    flask_thread.start()

    # Rodando o Telegram bot no processo principal
    telegram_bot()

if __name__ == '__main__':
    main()
