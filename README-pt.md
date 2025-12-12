[English Version](README.md)

# Animador de Papel de Parede da NASA

Um script em Python que busca imagens da câmera EPIC (Earth Polychromatic Imaging Camera) da NASA para uma data específica e as anima como um papel de parede dinâmico no desktop do Windows.

## Recursos

- Busca imagens de alta qualidade da Terra da API EPIC da NASA
- Baixa e armazena imagens localmente em cache para animação suave
- Anima o papel de parede em FPS personalizável (padrão 2 FPS)
- Interface de linha de comando simples
- Ferramenta educacional para visualizar a rotação da Terra

## Requisitos

- Python 3.x
- Biblioteca `requests` (`pip install requests`)
- Sistema operacional Windows (usa API do Windows para definir papel de parede)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/yourusername/nasa-wallpaper-animator.git
   cd nasa-wallpaper-animator
   ```

2. Instale as dependências:
   ```bash
   pip install requests
   ```

## Uso

Execute o script com argumentos opcionais:
```bash
python epic_wallpaper.py [--date AAAA-MM-DD] [--fps FPS] [--cache-dir DIR]
```

Opções:
- `--date`: Data no formato AAAA-MM-DD (padrão: 2024-12-07)
- `--fps`: Quadros por segundo (padrão: 0.5)
- `--cache-dir`: Diretório de cache (padrão: cache_nasa)

Exemplos:
```bash
# Usar data padrão com configurações padrão
python epic_wallpaper.py

# Usar uma data específica
python epic_wallpaper.py --date 2024-12-08

# FPS personalizado e diretório de cache
python epic_wallpaper.py --date 2024-12-07 --fps 1.0 --cache-dir meu_cache
```

O script irá:
1. Buscar imagens disponíveis para a data especificada
2. Baixar para o diretório de cache
3. Iniciar a animação do papel de parede em loop

Pressione Ctrl+C para parar a animação.

## Configuração

- Edite `api_test.py` para alterar a data ou variável FPS.
- As imagens são armazenadas em cache em `cache_nasa/` e limpas a cada execução.

## Informações da API

Usa a API EPIC da NASA: https://epic.gsfc.nasa.gov/api/natural

- Nenhuma chave de API necessária
- Imagens são de domínio público
- Limites de taxa podem se aplicar para solicitações frequentes

## Contribuição

Sinta-se à vontade para enviar issues ou pull requests para melhorias.

## Licença

Este projeto é open source. As imagens EPIC da NASA são de domínio público.