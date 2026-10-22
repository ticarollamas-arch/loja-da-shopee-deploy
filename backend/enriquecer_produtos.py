import sqlite3
import re
import time

print("🔄 Conectando ao banco para enriquecer títulos e hashtags...")
conn = sqlite3.connect('catalogo.db')
cursor = conn.cursor()

# Dicionário de sinônimos para substituição (Spintax)
sinonimos = {
    "conjunto": "kit", "blusa": "camisa", "feminina": "fem", "feminino": "fem",
    "masculino": "masc", "masculina": "masc", "calça": "calca", "vestido": "vestido",
    "plus size": "tamanho grande", "camiseta": "camisa", "tenis": "sapato esportivo",
    "sandalia": "chinelo", "brinco": "brinco", "colar": "colar", "anel": "anel",
    "perfume": "fragrancia", "bolsa": "bolsa", "mochila": "mochila", "relogio": "relogio",
    "infantil": "crianca", "adulto": "adulto", "promocao": "oferta", "luxo": "premium",
    "original": "autentico", "qualidade": "alta qualidade", "kit": "combo"
}

# Pega apenas os produtos BASE (sem o _V)
cursor.execute("SELECT id, titulo FROM produtos WHERE id NOT LIKE '%_V%'")
produtos_base = cursor.fetchall()

print(f"✅ {len(produtos_base)} produtos base encontrados. Iniciando enriquecimento...")
inicio = time.time()

for p in produtos_base:
    id_prod = p[0]
    titulo_original = p[1]
    
    # 1. Aplicar Spintax (Substituição de sinônimos no título)
    titulo_novo = titulo_original
    for velho, novo in sinonimos.items():
        # Substitui mantendo maiúsculas/minúsculas simples (regex case-insensitive)
        titulo_novo = re.sub(r'\b' + velho + r'\b', novo, titulo_novo, flags=re.IGNORECASE)
    
    # Capitalizar o título para ficar bonito
    titulo_novo = titulo_novo.title()
    
    # 2. Gerar Hashtags baseadas no título
    palavras = re.findall(r'\b[A-Za-zÀ-ÿ]{4,}\b', titulo_novo) # Pega palavras com 4+ letras
    # Pega as 3 primeiras palavras únicas e cria as hashtags
    palavras_unicas = list(dict.fromkeys(palavras))[:3]
    hashtags = " ".join([f"#{p}" for p in palavras_unicas])
    
    # Atualiza no banco
    cursor.execute('''
        UPDATE produtos 
        SET titulo = ? 
        WHERE id = ?
    ''', (f"{titulo_novo} {hashtags}", id_prod))

conn.commit()
conn.close()
fim = time.time()
print(f"🎉 Base de 63 mil produtos enriquecida em {fim - inicio:.2f} segundos!")
