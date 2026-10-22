import sqlite3, time
conn = sqlite3.connect('catalogo.db')
cursor = conn.cursor()

cursor.execute("SELECT id, titulo, preco, imagem, link, categoria FROM produtos")
produtos_base = cursor.fetchall()

variacoes = [
    " - Super Oferta", " - Promoção Imperdível", " - Frete Grátis Hoje", 
    " - Oferta do Dia", " - Melhor Preço do Ano", " - Achadinho Exclusivo", 
    " - Queima de Estoque", " - Desconto Relâmpago", " - Edição Limitada", " - Compre Agora"
]

print(f"🚀 Multiplicando {len(produtos_base)} produtos por 48...")
inicio = time.time()

for i in range(1, 49):
    lote_novo = []
    for p in produtos_base:
        novo_id = f"{p[0]}_V{i}"
        variacao = variacoes[(i - 1) % len(variacoes)]
        novo_titulo = f"{p[1]}{variacao}"
        # p[0]=id, p[1]=titulo, p[2]=preco, p[3]=imagem, p[4]=link, p[5]=categoria
        lote_novo.append((novo_id, novo_titulo, p[2], p[3], p[4], p[5]))
        
    cursor.executemany('INSERT OR IGNORE INTO produtos VALUES (?, ?, ?, ?, ?, ?)', lote_novo)
    conn.commit()
    
    if i % 10 == 0: print(f"   -> Lote {i}/48 inserido...")

conn.close()
print(f"🎉 Concluído em {time.time() - inicio:.2f} segundos!")
