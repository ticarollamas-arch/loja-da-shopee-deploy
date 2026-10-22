import sqlite3
import time

print("🔄 Conectando ao banco SQLite...")
conn = sqlite3.connect('catalogo.db')
cursor = conn.cursor()

# Como já temos 1 versão base, vamos criar mais 19 versões para dar 20x no total
MULTIPLICADOR = 19 

# Variações de título
variacoes = [
    " - Super Oferta", " - Promoção Imperdível", " - Frete Grátis Hoje", 
    " - Oferta do Dia", " - Melhor Preço do Ano", " - Achadinho Exclusivo", 
    " - Queima de Estoque", " - Desconto Relâmpago", " - Edição Limitada", 
    " - Compre Agora", " - Novidade", " - Top de Vendas", " - Tendência",
    " - Queima Total", " - Barato Demais", " - Destaque da Semana",
    " - Oportunidade Única", " - Corre que Acaba", " - Preço de Atacado"
]

# Pega apenas os produtos base (os que não têm _V no ID)
cursor.execute("SELECT id, titulo, preco, imagem, link, categoria FROM produtos WHERE id NOT LIKE '%_V%'")
produtos_base = cursor.fetchall()

print(f"✅ Produtos base encontrados: {len(produtos_base)}")
print(f"🚀 Iniciando multiplicação {MULTIPLICADOR}x direto no banco...")
inicio = time.time()

for i in range(1, MULTIPLICADOR + 1):
    lote_novo = []
    for p in produtos_base:
        novo_id = f"{p[0]}_V{i}"
        variacao = variacoes[(i - 1) % len(variacoes)]
        novo_titulo = f"{p[1]}{variacao}"
        
        lote_novo.append((novo_id, novo_titulo, p[2], p[3], p[4], p[5]))
        
    cursor.executemany('INSERT OR IGNORE INTO produtos VALUES (?, ?, ?, ?, ?, ?)', lote_novo)
    conn.commit()
    
    if i % 5 == 0:
        print(f"   -> Lote {i}/{MULTIPLICADOR} inserido...")

conn.close()
fim = time.time()
print(f"🎉 Concluído em {fim - inicio:.2f} segundos!")
