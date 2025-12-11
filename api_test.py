import os
import time
import ctypes
import requests
import glob

# Configurações
PASTA_CACHE = 'cache_nasa'
FPS = 0.5 # Tempo em segundos entre cada frame (0.5 = 2 frames por segundo)

# Cria a pasta de cache se não existir
if not os.path.exists(PASTA_CACHE):
    os.makedirs(PASTA_CACHE)

def limpar_cache():
    files = glob.glob(f"{PASTA_CACHE}/*.jpg")
    for f in files:
        os.remove(f)

def baixar_sequencia_do_dia(data_texto):
    """
    Baixa todas as fotos de um dia específico (formato YYYY-MM-DD)
    """
    print(f"📥 Baixando sequência de imagens para o dia: {data_texto}...")
    limpar_cache()
    
    # Busca os metadados
    url_api = f'https://epic.gsfc.nasa.gov/api/natural/date/{data_texto}'
    req = requests.get(url_api)
    
    if req.status_code != 200:
        print("Erro na API.")
        return []

    dados = req.json()
    if not dados:
        print("Nenhuma imagem encontrada neste dia.")
        return []

    caminhos_locais = []
    
    for i, item in enumerate(dados):
        nome_imagem = item['image']
        # Monta a data
        ano, mes, dia = data_texto.split('-')
        
        # URL JPG (Mais leve e rápido para animação que o PNG)
        url_download = f"https://epic.gsfc.nasa.gov/archive/natural/{ano}/{mes}/{dia}/jpg/{nome_imagem}.jpg"
        
        # Define o nome do arquivo local (00.jpg, 01.jpg) para manter a ordem
        caminho_arquivo = os.path.join(PASTA_CACHE, f"{i:02d}.jpg")
        caminho_absoluto = os.path.abspath(caminho_arquivo)
        
        print(f"   Baixando frame {i+1}/{len(dados)}...", end='\r')
        
        # Download
        resposta = requests.get(url_download)
        with open(caminho_arquivo, 'wb') as f:
            f.write(resposta.content)
            
        caminhos_locais.append(caminho_absoluto)

    print(f"\n✅ Download concluído! {len(caminhos_locais)} imagens prontas.")
    return caminhos_locais

def animar_wallpaper(lista_imagens):
    """
    Loop infinito que roda as imagens locais rapidamente
    """
    print("🎬 Iniciando a animação (Pressione Ctrl+C para parar)...")
    
    # Loop Infinito da Animação
    while True:
        for imagem in lista_imagens:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, imagem, 3)
            time.sleep(FPS) 

# --- EXECUÇÃO ---
if __name__ == "__main__":
    try:
        # Data fixa escolhida (um dia com céu limpo e muitas fotos)
        # Você pode mudar para uma data aleatória se quiser depois
        data_escolhida = '2024-12-07' 
        
        imagens = baixar_sequencia_do_dia(data_escolhida)
        
        if imagens:
            animar_wallpaper(imagens)
        
    except KeyboardInterrupt:
        print("\n🛑 Animação encerrada.")
    except Exception as e:
        print(f"\nErro: {e}")