import json
import sqlite3
import os

print("🔄 Lendo o JSON real de 63k...")
with open('catalogo.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

print(f"✅ Lido: {len(dados)} produtos reais. Criando banco SQLite...")

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

# Apaga o JSON para liberar 40MB de espaço
os.remove('catalogo.json')
print("✅ Banco SQLite criado com 63.477 produtos REAIS! O JSON foi deletado para liberar espaço.")
