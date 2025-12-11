import os
import time
import ctypes
import requests
import glob
import argparse
import logging
from datetime import date
from typing import List

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class NASAWallpaperDownloader:
    """Gerencia o download e cache das imagens EPIC da NASA."""

    def __init__(self, cache_dir: str = "cache_nasa") -> None:
        """
        Inicializa o downloader com um diretório de cache.

        Args:
            cache_dir: Diretório para armazenar imagens baixadas.
        """
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def clear_cache(self) -> None:
        """Limpa todos os arquivos JPG em cache."""
        files = glob.glob(os.path.join(self.cache_dir, "*.jpg"))
        for f in files:
            os.remove(f)

    def download_sequence(self, date_str: str) -> List[str]:
        """
        Baixa todas as imagens para uma data específica (formato AAAA-MM-DD).

        Args:
            date_str: Data no formato AAAA-MM-DD.

        Returns:
            Lista de caminhos absolutos para imagens baixadas.
        """
        logging.info(f"Baixando sequência de imagens para a data: {date_str}")
        self.clear_cache()

        # Buscar metadados
        api_url = f'https://epic.gsfc.nasa.gov/api/natural/date/{date_str}'
        try:
            response = download_with_retry(api_url)
            data = response.json()
        except requests.RequestException as e:
            logging.error(f"Falha ao buscar dados da API: {e}")
            return []

        if not data:
            logging.warning("Nenhuma imagem encontrada para esta data.")
            return []

        local_paths = []

        for i, item in enumerate(data):
            image_name = item['image']
            # Analisar data
            year, month, day = date_str.split('-')

            # URL JPG (mais leve e rápido para animação que PNG)
            base_url = "https://epic.gsfc.nasa.gov/archive/natural"
            download_url = (
                f"{base_url}/{year}/{month}/{day}/jpg/{image_name}.jpg"
            )

            # Nome do arquivo local (00.jpg, 01.jpg) para manter a ordem
            file_path = os.path.join(self.cache_dir, f"{i:02d}.jpg")
            absolute_path = os.path.abspath(file_path)

            logging.info(f"Baixando frame {i+1}/{len(data)}: {image_name}")

            try:
                # Download
                img_response = download_with_retry(download_url)
                with open(file_path, 'wb') as f:
                    f.write(img_response.content)
                local_paths.append(absolute_path)
            except requests.RequestException as e:
                logging.error(f"Falha ao baixar {image_name}: {e}")
                # Continuar para a próxima imagem

        logging.info(f"Download concluído! {len(local_paths)} imagens prontas.")
        return local_paths


class WallpaperAnimator:
    """Gerencia a animação do papel de parede no Windows."""

    def __init__(self, fps: float = 0.5) -> None:
        """
        Inicializa o animador com quadros por segundo.

        Args:
            fps: Tempo em segundos entre quadros (0.5 = 2 FPS).
        """
        self.fps = fps

    def animate(self, image_list: List[str]) -> None:
        """
        Executa loop infinito para alternar imagens como papel de parede.

        Args:
            image_list: Lista de caminhos de arquivos de imagem.
        """
        logging.info("Iniciando animação (Pressione Ctrl+C para parar)")

        # Loop infinito da animação
        while True:
            for image in image_list:
                try:
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
                except Exception as e:
                    logging.error(f"Falha ao definir papel de parede: {e}")
                time.sleep(self.fps)


def validate_date(date_str: str) -> bool:
    """
    Valida string de data no formato AAAA-MM-DD.

    Args:
        date_str: String de data a validar.

    Returns:
        True se válida, False caso contrário.
    """
    from datetime import datetime
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def download_with_retry(url: str, max_retries: int = 3) -> requests.Response:
    """
    Baixa URL com lógica de retry e backoff exponencial.

    Args:
        url: URL para baixar.
        max_retries: Número máximo de tentativas de retry.

    Returns:
        Objeto Response.

    Raises:
        requests.RequestException: Se todas as tentativas falharem.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Backoff exponencial
                logging.warning(f"Download falhou para {url}, tentando novamente em {wait_time}s... ({e})")
                time.sleep(wait_time)
            else:
                logging.error(f"Download falhou para {url} após {max_retries} tentativas: {e}")
                raise e


# --- EXECUÇÃO ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NASA Wallpaper Animator")
    parser.add_argument(
        '--date',
        type=str,
        default='2024-12-07',
        help='Date in YYYY-MM-DD format (default: 2024-12-07)'
    )
    parser.add_argument(
        '--fps',
        type=float,
        default=0.5,
        help='Frames per second (default: 0.5)'
    )
    parser.add_argument(
        '--cache-dir',
        type=str,
        default='cache_nasa',
        help='Cache directory (default: cache_nasa)'
    )

    args = parser.parse_args()

    # Validar formato da data
    if not validate_date(args.date):
        logging.error(f"Formato de data inválido: {args.date}. Use AAAA-MM-DD.")
        exit(1)

    try:
        downloader = NASAWallpaperDownloader(cache_dir=args.cache_dir)
        images = downloader.download_sequence(args.date)

        if images:
            animator = WallpaperAnimator(fps=args.fps)
            animator.animate(images)
        else:
            logging.info("Nenhuma imagem para animar.")

    except KeyboardInterrupt:
        logging.info("Animação parada pelo usuário.")
    except Exception as e:
        logging.exception(f"Erro inesperado: {e}")
