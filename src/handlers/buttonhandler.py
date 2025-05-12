
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext

from utils.database import con, cursor
from config import *
import requests
import time
from utils.comprar import comprar
from utils.comprar_sms import comprar_sms_sms_pva
from handlers.start import start
from handlers.ajuda import ajuda

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "serv" or query.data.startswith("ser_"):
        # Pega ou inicializa a página atual
        pagina = context.user_data.get("pagina_serv", 0)
        if query.data == "ser_next":
            pagina += 1
        elif query.data == "ser_prev" and pagina > 0:
            pagina -= 1
        context.user_data["pagina_serv"] = pagina

        # Buscar serviços da API
        header = { "apikey": API_SMS_ACTIVATE_KEY }
        response = requests.get("https://api.smspva.com/activation/servicesprices", headers=header)
        data = list(response.json()["data"])

        # Paginar (5 por página)
        inicio = pagina * 5
        fim = inicio + 5
        paginados = data[inicio:fim]

        keyboard = []
        for da in paginados:
            keyboard.append([
                InlineKeyboardButton(
                    f"{da['serviceDescription']}",
                    callback_data=f"serv_{da['service']}"
                )
            ])

        # Botões de navegação
        nav_buttons = []
        if pagina > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Anterior", callback_data="ser_prev"))
        if fim < len(data):
            nav_buttons.append(InlineKeyboardButton("➡️ Próximo", callback_data="ser_next"))
        if nav_buttons:
            keyboard.append(nav_buttons)

        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("https://api.smspva.com/activation/servicesprices\n\n📱 Escolha um serviço:", reply_markup=markup)

    elif query.data.startswith("serv_"):
        service_id = query.data.replace("serv_", "")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                userid INTEGER PRIMARY KEY,
                service TEXT DEFAULT 'None',
                pais TEXT DEFAULT 'None',
                saldo FLOAT DEFAULT 0.0,
                cpf TEXT DEFAULT 'None'
            )
        """)

        cursor.execute("SELECT * FROM user WHERE userid = ?", (update.effective_user.id,))
        data = cursor.fetchone()

        if data:
            cursor.execute("UPDATE user SET service = ? WHERE userid = ?", (service_id, update.effective_user.id))
        else:
            cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (update.effective_user.id, service_id, "None", 0))

        con.commit()
        await query.edit_message_text(f"Serviço `{service_id}` salvo com sucesso!", parse_mode="Markdown")
        time.sleep(3.5)
        await start(update, context)
    elif query.data.startswith("pais_") and not query.data.endswith("_next") and not query.data.endswith("_prev"):

        pais_id = query.data.replace("pais_", "")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                userid INTEGER PRIMARY KEY,
                service TEXT DEFAULT 'None',
                pais TEXT DEFAULT 'None',
                saldo FLOAT DEFAULT 0.0,
                cpf TEXT DEFAULT 'None'
            )
        """)

        cursor.execute("SELECT * FROM user WHERE userid = ?", (update.effective_user.id,))
        data = cursor.fetchone()

        if data:
            cursor.execute("UPDATE user SET pais = ? WHERE userid = ?", (pais_id, update.effective_user.id))
        else:
            cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (update.effective_user.id, "None", pais_id, 0))

        con.commit()
        await query.edit_message_text(f"Pais `{pais_id}` salvo com sucesso!", parse_mode="Markdown")
        time.sleep(3.5)
        await start(update, context)

    elif query.data == "pais" or query.data.startswith("pais_"):
        # Lista de países com códigos ISO
        lista_paises = [
            ("br", "Brasil"),
            ("us", "Estados Unidos"),
            ("ru", "Rússia"),
            ("in", "Índia"),
            ("cn", "China"),
            ("de", "Alemanha"),
            ("fr", "França"),
            ("gb", "Reino Unido"),
            ("it", "Itália"),
            ("es", "Espanha"),
            ("mx", "México"),
            ("ar", "Argentina"),
            ("jp", "Japão"),
            ("kr", "Coreia do Sul"),
            ("ca", "Canadá"),
            ("tr", "Turquia"),
            ("sa", "Arábia Saudita"),
            ("za", "África do Sul"),
            ("ng", "Nigéria"),
            ("eg", "Egito"),
        ]

        # Paginação
        pagina = context.user_data.get("pagina_serv", 0)  # Alterado de 'pagina_pais' para 'pagina_serv'
        if query.data == "pais_next":
            pagina += 1
        elif query.data == "pais_prev" and pagina > 0:
            pagina -= 1
        context.user_data["pagina_serv"] = pagina  # Alterado de 'pagina_pais' para 'pagina_serv'

        inicio = pagina * 5
        fim = inicio + 5
        paginados = lista_paises[inicio:fim]

        keyboard = []
        for codigo, nome in paginados:
            keyboard.append([
                InlineKeyboardButton(f"🌠 {nome} ({codigo.upper()})", callback_data=f"pais_{codigo}")
            ])

        # Botões de navegação
        nav_buttons = []
        if pagina > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Anterior", callback_data="pais_prev"))
        if fim < len(lista_paises):
            nav_buttons.append(InlineKeyboardButton("➡️ Próximo", callback_data="pais_next"))
        if nav_buttons:
            keyboard.append(nav_buttons)

        markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🌍 Escolha um país:", reply_markup=markup)
    elif query.data == "saldo":
        cursor.execute("SELECT saldo FROM user WHERE userid = ?", (update.effective_user.id,))
        resultado = cursor.fetchone()
        print(resultado)
        if resultado:
            saldo = resultado[0]

            await query.edit_message_text(f"💰 Seu saldo é de {saldo:.2f} BRL", parse_mode="Markdown")
            time.sleep(3.5)
            await start(update, context)
        else:
            await query.edit_message_text("❌ Usuário não encontrado ou saldo indisponível.")
            time.sleep(3.5)
            await start(update, context)
    elif query.data == "recarregar":
        await comprar(update, context)
    
    elif query.data == "sms":
        res = con.execute(f"SELECT * FROM user WHERE userid = {update.effective_user.id}")
        res = res.fetchone()
        if res[0]:
            code, numero = str(await comprar_sms_sms_pva(res[1], 1, res[2], update))
            cursor.execute("CREATE TABLE IF NOT EXISTS numeros (userid INT, numero VARCHAR(20), code VARCHAR(20))")
            cursor.executemany("INSERT INTO numeros VALUES (?, ?, ?)", update.effective_user.id, numero, code)
    elif query.data == "ativar":
        cursor.execute("CREATE TABLE IF NOT EXISTS numeros (userid INT, numero VARCHAR(20), code VARCHAR(20))")
        res = cursor.execute(f"SELECT * FROM numeros WHERE userid = {update._effective_user.id}")
        res = res.fetchall()
        if res:
            txt = ""

            for r in res:
                txt += f"\n\nNumero: {r[1]}\nCodigo: {r[2]}"
            if update.message:
                await update.message.reply_text(txt)
            else:
                await update.callback_query.edit_message_text(txt)
        else:
            txt = "Não há numeros comprados"
            if update.message:
                await update.message.reply_text(txt)
            else:
                await update.callback_query.edit_message_text(txt)
    elif query.data == "ajuda":
        await ajuda(update, context)
        
