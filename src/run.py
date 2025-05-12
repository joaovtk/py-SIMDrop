import threading
from bot import run_bot
from utils.webhook import *

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_webhook)
    flask_thread.daemon = True
    flask_thread.start()

    print("🚀 Iniciando bot e webhook...")
    run_bot()
