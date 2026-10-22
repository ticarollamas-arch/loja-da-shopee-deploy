import sqlite3
import re
import time

print("🔄 Conectando ao banco...")
conn = sqlite3.connect('catalogo.db')
cursor = conn.cursor()

# 1. Adiciona a coluna de hashtags se ela não existir
try:
    cursor.execute("ALTER TABLE produtos ADD COLUMN hashtags TEXT")
    print("✅ Coluna 'hashtags' criada no banco.")
except sqlite3.OperationalError:
    print("ℹ️ Coluna 'hashtags' já existe.")

# 2. Limpa todos os clones antigos (que estavam com hashtags no título)
print("🧹 Limpando clones antigos...")
cursor.execute("DELETE FROM produtos WHERE id LIKE '%_V%'")
conn.commit()

# 3. Pega os produtos base para reescrever
cursor.execute("SELECT id, titulo FROM produtos WHERE id NOT LIKE '%_V%'")
produtos_base = cursor.fetchall()

sinonimos = {
    "conjunto": "kit", "blusa": "camisa", "feminina": "fem", "feminino": "fem",
    "masculino": "masc", "masculina": "masc", "calça": "calca", "vestido": "vestido",
    "plus size": "tamanho grande", "camiseta": "camisa", "tenis": "sapato esportivo",
    "sandalia": "chinelo", "brinco": "brinco", "colar": "colar", "anel": "anel",
    "perfume": "fragrancia", "bolsa": "bolsa", "mochila": "mochila", "relogio": "relogio",
    "infantil": "crianca", "adulto": "adulto", "promocao": "oferta", "luxo": "premium",
    "original": "autentico", "qualidade": "alta qualidade", "kit": "combo"
}

print("✍️ Limpando títulos e gerando novas hashtags...")
for p in produtos_base:
    id_prod = p[0]
    titulo_original = p[1]
    
    # Remove qualquer hashtag antiga que tenha ficado no título (limpa tudo após o '#')
    titulo_limpo = re.sub(r'#\S+', '', titulo_original).strip()
    
    # Aplica sinônimos
    titulo_novo = titulo_limpo
    for velho, novo in sinonimos.items():
        titulo_novo = re.sub(r'\b' + velho + r'\b', novo, titulo_novo, flags=re.IGNORECASE)
    
    titulo_novo = titulo_novo.title() # Deixa as primeiras letras maiúsculas
    
    # Gera as hashtags baseadas nas palavras do título
    palavras = re.findall(r'\b[A-Za-zÀ-ÿ]{4,}\b', titulo_limpo)
    palavras_unicas = list(dict.fromkeys(palavras))[:4] # Pega 4 palavras
    hashtags = " ".join([f"#{p.capitalize()}" for p in palavras_unicas])
    
    # Atualiza o banco com o título limpo e as hashtags na coluna separada
    cursor.execute('''
        UPDATE produtos 
        SET titulo = ?, hashtags = ? 
        WHERE id = ?
    ''', (titulo_novo, hashtags, id_prod))

conn.commit()

# 4. Multiplicar 30x com os títulos novos
print("🚀 Multiplicando para 30x...")
variacoes = [
    " - Super Oferta", " - Promoção", " - Frete Grátis", " - Oferta do Dia", 
    " - Melhor Preço", " - Achadinho", " - Queima de Estoque", " - Desconto", 
    " - Edição Limitada", " - Compre Agora", " - Novidade", " - Top de Vendas", 
    " - Tendência", " - Barato", " - Destaque", " - Oportunidade", 
    " - Corre que Acaba", " - Atacado"
]

cursor.execute("SELECT id, titulo, preco, imagem, link, categoria, hashtags FROM produtos WHERE id NOT LIKE '%_V%'")
produtos_base_novos = cursor.fetchall()

for i in range(1, 30): # 29 lotes + 1 base = 30x
    lote_novo = []
    for p in produtos_base_novos:
        novo_id = f"{p[0]}_V{i}"
        variacao = variacoes[(i - 1) % len(variacoes)]
        novo_titulo = f"{p[1]}{variacao}"
        
        # p[0]=id, p[1]=titulo, p[2]=preco, p[3]=imagem, p[4]=link, p[5]=categoria, p[6]=hashtags
        lote_novo.append((novo_id, novo_titulo, p[2], p[3], p[4], p[5], p[6]))
        
    cursor.executemany('INSERT OR IGNORE INTO produtos VALUES (?, ?, ?, ?, ?, ?, ?)', lote_novo)
    conn.commit()
    if i % 10 == 0:
        print(f"   -> Lote {i}/29 inserido...")

conn.close()
print("🎉 Tudo pronto! Títulos limpos, hashtags no lugar certo e 1.9 milhões de produtos!")
