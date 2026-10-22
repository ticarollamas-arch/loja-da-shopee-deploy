import json
import sqlite3
import time
import random
import os

LOTE_POR_MINUTO = 1000
TEMPO_ESPERA = 60 # 1 minuto
ARQUIVO_BASE = 'produtos_base.json'

variacoes = [
    " - Super Oferta", " - Promoção Imperdível", " - Frete Grátis Hoje", 
    " - Oferta do Dia", " - Melhor Preço", " - Achadinho Exclusivo", 
    " - Queima de Estoque", " - Desconto Relâmpago", " - Compre Agora"
]

def iniciar():
    if not os.path.exists(ARQUIVO_BASE):
        print(f"❌ Arquivo {ARQUIVO_BASE} não encontrado! Baixe ele do Drive primeiro.")
        return

    print("🔄 Lendo a base dos 63k produtos...")
    with open(ARQUIVO_BASE, 'r', encoding='utf-8') as f:
        todos_produtos = json.load(f)

    # Filtra apenas produtos que têm título e link válidos (evita lixo)
    base_limpa = [p for p in todos_produtos if p.get('productName') and p.get('offerLink')]
    total_base = len(base_limpa)
    
    print(f"✅ Base lida com sucesso: {total_base} produtos válidos prontos para multiplicar.")
    print(f"🚀 Iniciando injeção de {LOTE_POR_MINUTO} produtos por minuto...")

    indice = 0
    ciclo = 1

    while True:
        conn = sqlite3.connect('catalogo.db')
        cursor = conn.cursor()
        lote_db = []
        
        # Pega um bloco de 1000 produtos
        for _ in range(LOTE_POR_MINUTO):
            p = base_limpa[indice % total_base]
            indice += 1
            
            # ID único para não duplicar no banco (Ex: 12345_V1)
            novo_id = f"{p.get('itemId', '')}_V{ciclo}"
            
            # Variação de título
            titulo = p.get('productName', '')
            if random.random() > 0.3:
                titulo += random.choice(variacoes)
                
            # Variação de imagem (usa a miniatura para o site ficar leve)
            img_url = p.get('imageUrl', '')
            if img_url and random.random() > 0.5:
                img_url = img_url.replace('_tn', '') + '_tn'

            lote_db.append((
                novo_id,
                titulo,
                float(p.get('priceMin', 0)),
                img_url,
                p.get('offerLink', ''),
                p.get('categoria', 'Geral')
            ))

        # Insere no SQLite
        cursor.executemany('INSERT OR IGNORE INTO produtos VALUES (?, ?, ?, ?, ?, ?)', lote_db)
        conn.commit()
        
        # Conta quantos tem no banco agora
        cursor.execute('SELECT count(*) FROM produtos')
        total_atual = cursor.fetchone()[0]
        conn.close()
        
        print(f"✅ Minuto {ciclo}: +1000 produtos inseridos. (Total no banco: {total_atual})")
        
        ciclo += 1
        time.sleep(TEMPO_ESPERA)

if __name__ == "__main__":
    iniciar()
