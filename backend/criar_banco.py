import sqlite3
conn = sqlite3.connect('catalogo.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id TEXT PRIMARY KEY,
        titulo TEXT,
        preco REAL,
        imagem TEXT,
        link TEXT,
        categoria TEXT
    )
''')
conn.commit()
conn.close()
print("✅ Banco de dados limpo e pronto para o garimpo real!")
