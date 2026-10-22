import json
print("🔄 Lendo o arquivo de 1.2GB...")
with open('catalogo.json', 'r', encoding='utf-8') as f:
    catalogo = json.load(f)[:300000] # Pega os primeiros 300k

print(f"✅ Cortado para {len(catalogo)} produtos. Salvando...")
with open('catalogo_otimizado.json', 'w', encoding='utf-8') as f:
    json.dump(catalogo, f, ensure_ascii=False, separators=(',', ':'))
print("✅ Pronto!")
