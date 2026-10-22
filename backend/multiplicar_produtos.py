import json
import random
import time

print("🔄 Lendo o banco de 63 mil produtos...")
with open('catalogo.json', 'r', encoding='utf-8') as f:
    catalogo_original = json.load(f)

print(f"✅ Lido: {len(catalogo_original)} produtos originais.")

# Variações de texto para tentar burlar a duplicação
variacoes = [
    " - Super Oferta", 
    " - Promoção Imperdível", 
    " - Frete Grátis", 
    " - Oferta do Dia", 
    " - Melhor Preço"
]

novo_catalogo = []

print("🚀 Multiplicando por 5... (isso pode demorar um pouco e usar muita RAM)")
inicio = time.time()

# Loop para criar as 5 cópias
for i in range(1, 6):
    print(f"   -> Gerando lote {i}...")
    for prod in catalogo_original:
        copia = prod.copy()
        
        # 1. Muda o ID para não dar conflito (ex: 12345_1)
        id_original = str(copia.get('itemId', ''))
        copia['itemId'] = f"{id_original}_{i}"
        
        # 2. Muda o título (adiciona a variação)
        titulo_original = copia.get('titulo', '')
        # Se for a primeira cópia, deixa o título original, nas outras adiciona variação
        if i > 1:
            copia['titulo'] = f"{titulo_original}{variacoes[i-2]}"
            
        novo_catalogo.append(copia)

print(f"✅ Total de produtos gerados: {len(novo_catalogo)}")
print("💾 Salvando o novo catalogo.json...")

# Faz um backup do original antes de sobrescrever
import shutil
shutil.copy('catalogo.json', 'catalogo_63k_original.json')

# Salva o novo banco
with open('catalogo.json', 'w', encoding='utf-8') as f:
    json.dump(novo_catalogo, f, ensure_ascii=False, indent=2)

fim = time.time()
print(f"🎉 Concluído em {fim - inicio:.2f} segundos!")
