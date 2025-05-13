
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
from telegram.constants import ParseMode

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
                    callback_data=f"serv_{da['service']}-{da['serviceDescription']}-{da['price']}"
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
        res = query.data.replace("serv_", "")
        res = res.split("-")
        print(res)
        service_id = res[0]
        nome = res[1]
        price = res[2]
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                userid INTEGER PRIMARY KEY,
                service TEXT DEFAULT 'None',
                pais TEXT DEFAULT 'None',
                saldo FLOAT DEFAULT 0.0
            )
        """)

        keyboard = [
            [InlineKeyboardButton("🌟 Favoritar", callback_data=f"favserv_{service_id}-{nome}-{price}")],
            [InlineKeyboardButton("📣 Definir Como padrão", callback_data=f"setserv_{service_id}")],
            [InlineKeyboardButton("👟 Voltar ao menu Start", callback_data="exit")]
        ]
        markup = InlineKeyboardMarkup(keyboard)

        cursor.execute("SELECT * FROM user WHERE userid = ?", (update.effective_user.id,))
        data = cursor.fetchone()

        if data:
            cursor.execute("UPDATE user SET service = ? WHERE userid = ?", (service_id, update.effective_user.id))
        else:
            cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (update.effective_user.id, service_id, "None", 0))
        con.commit()
        await query.edit_message_text(f"Nome do Serviço: {nome}\n\nPreço do serviço: ${price}\n\nPara salvar o serviço com padrão no botão Escolher Serviço\nPara favoritar clique no botão Favoritar", parse_mode="Markdown", reply_markup=markup)
    elif query.data.startswith("pais_") and not query.data.endswith("_next") and not query.data.endswith("_prev"):

        pais_id = query.data.replace("pais_", "")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                userid INTEGER PRIMARY KEY,
                service TEXT DEFAULT 'None',
                pais TEXT DEFAULT 'None',
                saldo FLOAT DEFAULT 0.0
            )

        """)
        con.commit()
        keyboard = [
            [InlineKeyboardButton("⭐ Favoritar", callback_data=f"fav_pais{pais_id}")],
            [InlineKeyboardButton("📣 Definir Como padrão", callback_data=f"setpais_{pais_id}")]
        ]

        markup = InlineKeyboardMarkup(keyboard)

        con.commit()
        await query.edit_message_text(f"**Codigo do pais**: `{pais_id}`\n\n\n\n", parse_mode="Markdown", reply_markup=markup)

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
            keyboard = [
                    [InlineKeyboardButton("👟 Voltar ao menu Start", callback_data="exit")]
                ]
            markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"💰 Seu saldo é de `{saldo:.2f} BRL`", parse_mode="Markdown", reply_markup=markup)

        else:
            await query.edit_message_text("❌ Usuário não encontrado ou saldo indisponível.")
            time.sleep(3.5)
            await start(update, context)
    elif query.data == "recarregar":
        await comprar(update, context)
    
    elif query.data == "sms":
        res = con.execute(f"SELECT * FROM user WHERE userid = {update.effective_user.id}")
        res = res.fetchone()
        print(res)
        if res[1] == "None" and res[2] == "None":
            if update.message:
                await update.message.reply_text("Selecione o pais e o Serviço padrão no menu /start")
            else:
                await update.callback_query.edit_message_text("Selecione o pais e o Serviço padrão no menu start")
        else:
            if res[3] > 0.0:
                response = str(await comprar_sms_sms_pva(res[1], 1, res[2], update))
                print(response)
                if (response):
                    if update.message:
                        await update.message.reply_text("Houve um erro no processo de compra de numero")
                    else:
                        await update.callback_query.edit_message_text("Houve um erro no processo de compra de numero")
                else:
                    keyboard = [
                        [InlineKeyboardButton("👟 Voltar ao menu Start", callback_data="exit")]
                    ]
                    markup = InlineKeyboardMarkup(keyboard)
                    cursor.execute("CREATE TABLE IF NOT EXISTS numeros (userid INT, numero VARCHAR(20), code VARCHAR(20))")
                    cursor.executemany("INSERT INTO numeros VALUES (?, ?, ?)", update.effective_user.id, response["numero"], response["code"])
                    if update.message:
                        await update.message.reply_text("✅ Numero Comprado Com sucesso", reply_markup=markup)
                    else:
                        await update.callback_query.edit_message_text("✅ Numero Comprado Com sucesso\nFoi debitado do saldo 1 real", reply_markup=markup)
            else:
                keyboard = [
                    [InlineKeyboardButton("👟 Voltar ao menu Start", callback_data="exit")]
                ]
                markup = InlineKeyboardMarkup(keyboard)
                await update.callback_query.edit_message_text("💵 Você não tem saldo no banco de dados volte para `/start` para adicionar saldo via pix ", parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
    elif query.data == "ativar":
        cursor.execute("CREATE TABLE IF NOT EXISTS numeros (userid INT, numero VARCHAR(20), code VARCHAR(20))")
        res = cursor.execute(f"SELECT * FROM numeros WHERE userid = {update._effective_user.id}")
        res = res.fetchall()
        keyboard = [
                [InlineKeyboardButton("👟 Voltar ao menu Start", callback_data="exit")]
            ]
        markup = InlineKeyboardMarkup(keyboard)
        if res:
            txt = ""

            for r in res:
                txt += f"\n\nNumero: {r[1]}\nCodigo: {r[2]}"
            if update.message:
                await update.message.reply_text(txt)
            else:
                await update.callback_query.edit_message_text(txt, reply_markup=markup)
        else:
            txt = "❌ Não há numeros comprados"
            if update.message:
                await update.message.reply_text(txt)
            else:
                await update.callback_query.edit_message_text(txt, reply_markup=markup)
            
    elif query.data == "duvidas":
        keyboard = [
            [InlineKeyboardButton("👟 Voltar ao menu Start", callback_data="exit")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.edit_message_text("📚 *Central de Dúvidas - Suporte ao Usuário*\n\n🔹 *1. Como funciona a compra de número virtual?* Você escolhe o serviço (ex: WhatsApp, Telegram), o país desejado e realiza o pagamento. Após o pagamento ser confirmado, um número virtual será entregue automaticamente.\n\n🔹 *2. Quais serviços estão disponíveis?* Atualmente suportamos: WhatsApp, Telegram, Google, Instagram, Facebook, TikTok e outros. Verifique a lista atualizada no comando /servicos.\n\n🔹 *3. Como faço um pagamento?* Aceitamos Pix via QR Code. Você verá os dados de pagamento após escolher o serviço e o país no Botão **Comprar Numero**\n\n🔹 *4. Quanto tempo demora para receber o número?* Geralmente, o número é entregue em poucos segundos após o pagamento. Em casos raros, pode levar até 2 minutos.\n\n🔹 *5. E se o número não receber o SMS?* Se o número não receber o SMS em até 10 minutos você deve entrar em contato com o suporte.\n\n🔹 *6. O que acontece se eu pagar e não usar o número?* Você pode manter o saldo no bot para usar depois. Mas os números entregues não podem ser reutilizados ou trocados após gerados.\n\n🔹 *7. Como posso ver meu saldo?* Use o /start e use o botão **Ver Saldo**\n\n❓ *Ainda com dúvidas?* Entre em contato com o suporte ou envie uma mensagem aqui mesmo. Estamos prontos para te ajudar!", parse_mode="Markdown", reply_markup=markup)
    elif query.data == "exit":
        await start(update, context)
    elif query.data == "ajuda":
        await ajuda(update, context)

    elif query.data == "erase":
        if context.user_data.get("msg_user_id"):
            await update.callback_query.delete_message()
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.user_data.get("msg_user_id"))

    elif query.data.startswith("favserv_"):
        res = query.data.replace("favserv_", "")
        res = res.split("-")
        nome = res[1]
        id = res[0]
        price = res[2]
        cursor.execute("CREATE TABLE IF NOT EXISTS fav (userid INT, servico VARCHAR(20), pais VARCHAR(20), servicoId VARCHAR(20), price FLOAT)")
        cursor.execute("SELECT servico FROM fav WHERE userid = ? AND servico = ?", (update.effective_user.id, nome))
        data = cursor.fetchone()

        if data:
            cursor.execute(f"UPDATE fav SET servico = {nome} WHERE userid = {update.effective_user.id}")
        else:
            cursor.execute(f"INSERT INTO fav VALUES (?, ?, ?, ?, ?)", (update.effective_user.id , nome, "None", id, price))
        con.commit()

        await update.callback_query.edit_message_text("🌟 Serviço favoritado com sucesso")
        time.sleep(3.5)
        await start(update, context)
    elif query.data.startswith("favorito_serv"):
        cursor.execute("SELECT servico, price FROM fav WHERE userid = ?", (update.effective_user.id,))
        data = cursor.fetchall()

        txt = "🌟 Serviços Favoritados:\n\n"
        keyboard = [
            [InlineKeyboardButton("👟 Voltar ao menu Start", callback_data="exit")]
        ]
        markup = InlineKeyboardMarkup(keyboard)

        if data:
            for servico, price in data:
                if servico != "None":
                    txt += f"📱 **Nome do Serviço**: `{servico}`\n\n💲 Preço: *{price:.2f}*\n\n\n\n"
                else:
                    txt = "❌ Não há serviços favoritados"
            if update.message:
                await update.message.reply_text(txt, parse_mode="Markdown", reply_markup=markup)
            else:
                await update.callback_query.edit_message_text(txt, parse_mode="Markdown", reply_markup=markup)
        else:
            txt = "❌ Você ainda não tem nenhum serviço favoritado."
            if update.message:
                await update.message.reply_text(txt)
            else:
                await update.callback_query.edit_message_text(txt)
    elif query.data.startswith("favorito_pais"):
        cursor.execute("SELECT pais FROM fav WHERE userid = ?", (update.effective_user.id,))
        data = cursor.fetchall()
        print(data)

        txt = "🌟 Serviços Favoritados:\n\n"
        keyboard = [
            [InlineKeyboardButton("👟 Voltar ao menu Start", callback_data="exit")]
        ]
        markup = InlineKeyboardMarkup(keyboard)

        if data:
            for da in data:
                if da[0] != "None":
                    txt += f"📱 **Codigo do Pais**: `{da[0]}`\n\n"
                else:
                    txt = "❌ *Você ainda não tem nenhum país favoritado.* Adicione países aos seus favoritos para acessá-los rapidamente"

                    break
            if update.message:
                await update.message.reply_text(txt, parse_mode="Markdown", reply_markup=markup)
            else:
                await update.callback_query.edit_message_text(txt, parse_mode="Markdown", reply_markup=markup)
        else:
            txt = "❌ *Você ainda não tem nenhum país favoritado.* Adicione países aos seus favoritos para acessá-los rapidamente."
            if update.message:
                await update.message.reply_text(txt, parse_mode="Markdown")
            else:
                await update.callback_query.edit_message_text(txt, parse_mode="Markdown")

    elif query.data.startswith("fav_pais"):
        print(query.data)
        res = query.data.replace("fav_pais", "")
        res = res.split("-")
        
        code = res[0]

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fav (
                userid INT,
                servico VARCHAR(20),
                pais VARCHAR(20),
                servicoId VARCHAR(20),
                price FLOAT
            )
        """)
        
        # Verifica se o país já foi favoritado
        cursor.execute("SELECT pais FROM fav WHERE userid = ? AND pais = ?", (update.effective_user.id, code))
        data = cursor.fetchone()

        if not data:
            cursor.execute("INSERT INTO fav VALUES (?, ?, ?, ?, ?)", (update.effective_user.id, "None", code, "None", 0.0))
            con.commit()
            await update.callback_query.edit_message_text("🌟 *País favoritado com sucesso!* Agora você pode acessar facilmente este país a partir da seção de favoritos.")
        else:
            await update.callback_query.edit_message_text("✅ *País já está nos seus favoritos!* Você já adicionou este país anteriormente. Para visualizar ou gerenciar seus favoritos, acesse a seção correspondente.", parse_mode="Markdown")

        time.sleep(3.5)
        await start(update, context)
    elif query.data.startswith("setpais_"):
        data = cursor.execute("SELECT * FROM user WHERE userid = ?", (update.effective_user.id,))
        data = data.fetchone()
        res = query.data.replace("setpais_", "")
        pais_id = res

        if data:
            cursor.execute(f"UPDATE user SET pais = ? WHERE userid = ?", (pais_id, update.effective_user.id))
        else:
            cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (update.effective_user.id, pais_id, "None", 0.00))
        await update.callback_query.edit_message_text("✅ *País definido como padrão com sucesso!*A partir de agora, esse país será selecionado automaticamente nas suas próximas compras. Você pode alterá-lo a qualquer momento escolhendo outro país na lista.", parse_mode="Markdown")
        time.sleep(3.5)
        await start(update, context)
        con.commit()
    elif query.data.startswith("setserv_"):
        data = cursor.execute("SELECT * FROM user WHERE userid = ?", (update.effective_user.id))
        data = data.fetchone()
        res = query.data.replace("setserv_", "")
        se_id = res

        if data:
            cursor.execute(f"UPDATE user SET service = ? WHERE userid = ?", (service_id, update.effective_user.id))
        else:
            cursor.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (update.effective_user.id, service_id, "None", 0.00))
        await update.callback_query.edit_message_text("✅ *Serviço definido como padrão com sucesso!* A partir de agora, este serviço será selecionado automaticamente nas suas próximas compras. Você pode trocá-lo quando quiser, escolhendo outro serviço na lista. 📱", parse_mode="Markdown")
        time.sleep(3.5)
        await start(update, context)
        con.commit()