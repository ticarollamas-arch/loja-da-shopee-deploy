import os
import json
import sqlite3
import time
import subprocess
import random

TOTAL_LOTES = 33
ARQUIVO_JSON_WORKER = 'catalogo.json'
ARQUIVO_LOTE = 'lote_atual.json'

variacoes_titulo = [
    " - Novo", " - Promoção", " - Achadinho", " - Top", " - Oferta",
    " - Imperdível", " - Barato", " - Tendência", " - Destaque"
]

def processar_e_salvar():
    if not os.path.exists(ARQUIVO_JSON_WORKER):
        print("⚠️ Worker não gerou o catalogo.json neste minuto.")
        return

    # Renomeia o arquivo para evitar que o worker sobrescreva enquanto lemos
    os.rename(ARQUIVO_JSON_WORKER, ARQUIVO_LOTE)

    try:
        with open(ARQUIVO_LOTE, 'r', encoding='utf-8') as f:
            novos = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler JSON: {e}")
        os.remove(ARQUIVO_LOTE)
        return

    if not novos:
        os.remove(ARQUIVO_LOTE)
        print("⚠️ Lote vazio.")
        return

    conn = sqlite3.connect('catalogo.db')
    cursor = conn.cursor()
    lote_db = []

    for p in novos:
        img_url = p.get('imageUrl', '')
        if img_url:
            img_url = img_url.replace('_tn', '') + '_tn' 

        titulo_original = p.get('productName', 'Produto')
        if random.random() > 0.5:
            titulo_original += random.choice(variacoes_titulo)

        lote_db.append((
            str(p.get('itemId', '')),
            titulo_original,
            float(p.get('priceMin', 0)),
            img_url,
            p.get('offerLink', ''),
            p.get('categoria', 'Geral')
        ))

    cursor.executemany('INSERT OR IGNORE INTO produtos VALUES (?, ?, ?, ?, ?, ?)', lote_db)
    conn.commit()
    conn.close()
    
    os.remove(ARQUIVO_LOTE)
    print(f"✅ Lote de {len(novos)} produtos inserido no SQLite!")

print("🚀 Iniciando a Operação de 33 Minutos!")

for i in range(1, TOTAL_LOTES + 1):
    print(f"\n⏱️ Minuto {i}/{TOTAL_LOTES} - Rodando o garimpeiro...")
    
    # Roda o worker por 50 segundos
    subprocess.run(['timeout', '50s', 'node', 'worker-categorias.js'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Processa o que foi baixado
    processar_e_salvar()
    
    if i < TOTAL_LOTES:
        time.sleep(10)

print("\n🎉 OPERAÇÃO DE 33 MINUTOS CONCLUÍDA!")
