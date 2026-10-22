import sqlite3
import time
import os

print("🚀 Iniciando a Operação 10 Milhões (Modo Seguro)...")
conn = sqlite3.connect('catalogo.db')
cursor = conn.cursor()

# Já temos de 1 a 29. Vamos do 30 ao 158 (Total = 158x * 63.477 = 10.029.366 produtos)
LOTES_FALTANTES = range(30, 159)

variacoes = [
    " - Super Oferta", " - Promoção", " - Frete Grátis", " - Oferta do Dia", 
    " - Melhor Preço", " - Achadinho", " - Queima de Estoque", " - Desconto", 
    " - Edição Limitada", " - Compre Agora", " - Novidade", " - Top de Vendas", 
    " - Tendência", " - Barato", " - Destaque", " - Oportunidade", 
    " - Corre que Acaba", " - Atacado", " - Oferta Relâmpago", " - Liquidificação"
]

# Pega a base de 63 mil produtos (apenas uma vez para não sobrecarregar a RAM)
cursor.execute("SELECT id, titulo, preco, imagem, link, categoria, hashtags FROM produtos WHERE id NOT LIKE '%_V%'")
produtos_base = cursor.fetchall()
print(f"✅ Base carregada: {len(produtos_base)} produtos.")

contador_lote = 0
inicio = time.time()

for i in LOTES_FALTANTES:
    lote_novo = []
    for p in produtos_base:
        novo_id = f"{p[0]}_V{i}"
        variacao = variacoes[(i - 1) % len(variacoes)]
        novo_titulo = f"{p[1]}{variacao}"
        lote_novo.append((novo_id, novo_titulo, p[2], p[3], p[4], p[5], p[6]))
        
    cursor.executemany('INSERT OR IGNORE INTO produtos VALUES (?, ?, ?, ?, ?, ?, ?)', lote_novo)
    conn.commit()
    
    contador_lote += 1
    print(f"   -> Lote {i} inserido. ({contador_lote}/{len(LOTES_FALTANTES)})")
    
    # PAUSA TÉRMICA: A cada 5 lotes (300 mil produtos), dorme 10 segundos
    if contador_lote % 5 == 0:
        print("   🧊 Pausa térmica de 10 segundos para o celular respirar...")
        time.sleep(10)
        # Verifica o tamanho do banco a cada pausa
        tamanho_db = os.path.getsize('catalogo.db') / (1024 * 1024 * 1024)
        print(f"   💾 Tamanho atual do banco: {tamanho_db:.2f} GB")

conn.close()
fim = time.time()
print(f"🎉 OPERAÇÃO 10 MILHÕES CONCLUÍDA em {(fim - inicio)/60:.2f} minutos!")
