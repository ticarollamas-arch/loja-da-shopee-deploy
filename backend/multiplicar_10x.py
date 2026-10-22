import json
import time
import shutil
import os

print("🔄 Lendo o banco atual de 317 mil produtos...")
inicio = time.time()

# Lendo o arquivo
with open('catalogo.json', 'r', encoding='utf-8') as f:
    catalogo_original = json.load(f)

print(f"✅ Lido: {len(catalogo_original)} produtos. Iniciando multiplicação 10x...")

# Variações de texto (10 sufixos diferentes)
variacoes = [
    " - Super Oferta", 
    " - Promoção Imperdível", 
    " - Frete Grátis Hoje", 
    " - Oferta do Dia", 
    " - Melhor Preço do Ano",
    " - Achadinho Exclusivo",
    " - Queima de Estoque",
    " - Desconto Relâmpago",
    " - Edição Limitada",
    " - Compre Agora"
]

# O arquivo vai ficar muito grande, então usaremos um gerador em vez de salvar tudo na RAM.
# Primeiro, vamos deletar o arquivo atual para liberar espaço em disco antes de criar o novo
os.remove('catalogo.json')

# Abre o arquivo para escrita no modo streaming
with open('catalogo_novo.json', 'w', encoding='utf-8') as f_out:
    f_out.write('[\n')
    
    total_gerado = 0
    for i in range(1, 11): # 10 vezes
        print(f"   -> Gerando lote {i}/10...")
        for index, prod in enumerate(catalogo_original):
            copia = prod.copy()
            
            # Muda o ID (ex: 123_1_1)
            id_orig = str(copia.get('itemId', ''))
            copia['itemId'] = f"{id_orig}_V{i}"
            
            # Muda o título
            titulo_orig = copia.get('titulo', '')
            copia['titulo'] = f"{titulo_orig}{variacoes[i-1]}"
            
            # Escreve no arquivo sem indentação (economiza espaço)
            json.dump(copia, f_out, ensure_ascii=False, separators=(',', ':'))
            
            total_gerado += 1
            
            # Adiciona vírgula se não for o último item
            if not (i == 10 and index == len(catalogo_original) - 1):
                f_out.write(',\n')
                
    f_out.write('\n]')

# Renomeia o arquivo final
os.rename('catalogo_novo.json', 'catalogo.json')

fim = time.time()
print(f"🎉 Concluído! Total gerado: {total_gerado} produtos em {fim - inicio:.2f} segundos.")
