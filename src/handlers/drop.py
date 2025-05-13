from telegram import Update
from telegram.ext import ContextTypes
from utils.database import con, cursor

async def drop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("DROP TABLE usuarios")
    cursor.execute("DROP TABLE numeros")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            userid INTEGER PRIMARY KEY,
            service TEXT DEFAULT 'None',
            pais TEXT DEFAULT 'None',
            saldo FLOAT DEFAULT 0.0
        )
    """)
    cursor.execute("CREATE TABLE IF NOT EXISTS numeros (userid INT, numero VARCHAR(20), code VARCHAR(20))")
    con.commit()
