import sqlite3
import os

# Conexão com banco de dados SQLite
con = sqlite3.connect("main.db", check_same_thread=False)
cursor = con.cursor()

# Criar tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user (
        userid INTEGER PRIMARY KEY,
        service TEXT DEFAULT 'None',
        pais TEXT DEFAULT 'None',
        saldo FLOAT DEFAULT 0.0,
        cpf TEXT DEFAULT 'None'
    )
""")
cursor.execute("CREATE TABLE IF NOT EXISTS numeros (userid INT, numero VARCHAR(20), code VARCHAR(20))")
con.commit()
