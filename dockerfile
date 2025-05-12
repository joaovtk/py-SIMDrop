# Usa uma imagem base com Python
FROM python:3.11-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia a pasta src para dentro do container
COPY src ./src

# Instala as dependências, se houver um requirements.txt
# Descomente a linha abaixo se você tiver esse arquivo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 5000
EXPOSE 5000
# Comando para iniciar o bot
CMD ["python", "src/bot.py"]
