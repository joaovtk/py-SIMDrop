import requests
import time

def send_ping():
    while True:
        try:
            requests.get('http://localhost:5000/ping')  # Substitua pela URL do seu bot
            print("Ping enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar ping: {e}")
        
        time.sleep(300)  # Aguarda 5 minutos (300 segundos)