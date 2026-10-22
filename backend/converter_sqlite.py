import json
import sqlite3
import os

print("🔄 Lendo o JSON...")
with open('catalogo.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

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

lote = []
for p in dados:
    lote.append((
        str(p.get('itemId', '')),
        p.get('productName', ''),
        float(p.get('priceMin', 0)),
        p.get('imageUrl', ''),
        p.get('offerLink', ''),
        p.get('categoria', 'Geral')
    ))

cursor.executemany('INSERT OR REPLACE INTO produtos VALUES (?, ?, ?, ?, ?, ?)', lote)
conn.commit()
conn.close()
os.remove('catalogo.json')
print("✅ Banco SQLite recriado com categorias!")
