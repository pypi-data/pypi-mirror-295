import json
import os
import subprocess
import zipfile

import toml
from pathlib3x import Path
from playwright.async_api import async_playwright
from rich.console import Console

from worker_automate_hub.config.settings import (
    get_package_version,
    load_env_config,
)
from worker_automate_hub.utils.logger import logger

console = Console()


def write_env_config(env_dict: dict, google_credentials: dict):
    try:
        current_dir = Path.cwd()
        assets_path = current_dir / "assets"
        logs_path = current_dir / "logs"
        assets_path.mkdir(exist_ok=True)
        logs_path.mkdir(exist_ok=True)

        config_file_path = current_dir / "settings.toml"
        config_data = {
            "name": "WORKER",
            "params": {
                "api_base_url": env_dict["API_BASE_URL"],
                "api_auth": env_dict["API_AUTHORIZATION"],
                "notify_alive_interval": env_dict["NOTIFY_ALIVE_INTERVAL"],
                "version": get_package_version("worker-automate-hub"),
                "log_level": env_dict["LOG_LEVEL"],
                "drive_url": env_dict["DRIVE_URL"],
            },
            "google_credentials": google_credentials["content"],
        }

        with open(config_file_path, "w") as config_file:
            toml.dump(config_data, config_file)

        log_msg = f"Arquivo de configuração do ambiente criado em {config_file_path}"
        logger.info(log_msg)
        console.print(f"\n{log_msg}\n", style="green")

        return {
            "Message": log_msg,
            "Status": True,
        }
    except Exception as e:
        err_msg = f"Erro ao criar o arquivo de configuração do ambiente. Comando retornou: {e}"
        logger.error(err_msg)
        return {
            "Message": err_msg,
            "Status": False,
        }


def add_worker_config(worker):
    try:
        current_dir = Path.cwd()
        config_file_path = current_dir / "settings.toml"

        if not config_file_path.exists():
            raise FileNotFoundError(
                f"O arquivo de configuração não foi encontrado em: {config_file_path}"
            )

        with open(config_file_path, "r") as config_file:
            config_data = toml.load(config_file)

        config_data["id"] = {
            "worker_uuid": worker["uuidRobo"],
            "worker_name": worker["nomRobo"],
        }

        with open(config_file_path, "w") as config_file:
            toml.dump(config_data, config_file)

        log_msg = f"Informações do worker adicionadas ao arquivo de configuração em {config_file_path}"
        console.print(f"\n{log_msg}\n", style="green")
        return {
            "Message": log_msg,
            "Status": True,
        }
    except Exception as e:
        err_msg = f"Erro ao adicionar informações do worker ao arquivo de configuração.\n Comando retornou: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        return {
            "Message": err_msg,
            "Status": False,
        }


async def install_playwright():
    try:
        result1 = subprocess.run(
            ["pipx", "install", "playwright"],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info(result1.stdout)
        result2 = subprocess.run(
            ["playwright", "install"], check=True, capture_output=True, text=True
        )
        logger.info("Playwright instalado com sucesso!")
        logger.info(result2.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao instalar Playwright: {e}")


def extract_zip(zip_path, extract_to):
    """
    Extrai um arquivo ZIP para um diretório especificado.

    :param zip_path: Caminho para o arquivo ZIP.
    :param extract_to: Diretório onde os arquivos serão extraídos.
    """
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
        console.print(f"\nArquivos extraídos para {extract_to}\n", style="green")


async def download_assets_and_extract_from_drive():
    try:
        console.print("\nIniciando download dos assets...\n", style="bold green")
        env_config, creds_loaded = load_env_config()
        creds_loaded = json.loads(creds_loaded)["web"]
        folder_url = env_config["DRIVE_URL"]

        # Diretório de execução atual
        current_dir = Path.cwd()
        output_folder = current_dir / "assets"
        destination_path = current_dir / "temp.zip"

        if not output_folder.exists():
            output_folder.mkdir(parents=True, exist_ok=True)

        await install_playwright()

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True
            )  # Defina headless=True se não quiser ver o navegador
            context = await browser.new_context()

            # Abrir uma nova página
            page = await context.new_page()

            # Navegar para a URL do arquivo no Google Drive
            await page.goto(folder_url)

            # Aguarde o carregamento da página e clique no botão de download
            await page.wait_for_selector(
                "#drive_main_page > div > div.g3Fmkb > div.S630me > div > div > div > div:nth-child(2) > div > div:nth-child(1) > div > div > div.a-s-tb-sc-Ja-Q.a-s-tb-sc-Ja-Q-Nm.a-Ba-Ed.a-s-Ba-dj > div > div.h-sb-Ic.h-R-d.a-c-d.a-r-d.a-R-d.a-s-Ba-d-Mr-Be-nAm6yf",
                timeout=60000,
            )
            await page.click(
                "#drive_main_page > div > div.g3Fmkb > div.S630me > div > div > div > div:nth-child(2) > div > div:nth-child(1) > div > div > div.a-s-tb-sc-Ja-Q.a-s-tb-sc-Ja-Q-Nm.a-Ba-Ed.a-s-Ba-dj > div > div.h-sb-Ic.h-R-d.a-c-d.a-r-d.a-R-d.a-s-Ba-d-Mr-Be-nAm6yf"
            )

            # Aguarde o download começar
            download = await page.wait_for_event("download")

            # Salve o arquivo no destino especificado
            await download.save_as(destination_path)

            await browser.close()

        extract_zip(destination_path, current_dir)
        os.remove(destination_path)

        console.print("\nAssets baixados com sucesso!\n", style="bold green")
    except Exception as e:
        err_msg = f"Erro ao baixar os assets: {e}"
        logger.error(err_msg)
        console.print(f"\n{err_msg}\n", style="bold red")


async def install_tesseract(setup_path: Path):
    try:
        # Comando para executar com elevação
        command = f'start-process "{setup_path}" -Verb runAs'

        # Executar o comando usando PowerShell
        result = subprocess.run(
            ["powershell", "-Command", command], capture_output=True
        )
        logger.info(result.stdout)
        logger.info("Tesseract instalado com sucesso!")
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao instalar Tesseract: {e}")


async def download_tesseract():
    # Diretório de execução atual
    current_dir = Path.cwd()
    output_folder = current_dir / "temp"
    destination_path = output_folder / "tesseract.exe"

    folder_url = "https://github.com/UB-Mannheim/tesseract/wiki"
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True
        )  # Defina headless=True se não quiser ver o navegador
        context = await browser.new_context()

        # Abrir uma nova página
        page = await context.new_page()

        # Navegar para a URL do arquivo no Google Drive
        await page.goto(folder_url)

        # Aguarde o carregamento da página e clique no botão de download
        await page.wait_for_selector(
            "#wiki-body > div > ul:nth-child(7) > li > a",
            timeout=60000,
        )
        await page.click("#wiki-body > div > ul:nth-child(7) > li > a")

        # Aguarde o download começar
        download = await page.wait_for_event("download")

        # Salve o arquivo no destino especificado
        await download.save_as(destination_path)

        await browser.close()

    await install_tesseract(destination_path)
