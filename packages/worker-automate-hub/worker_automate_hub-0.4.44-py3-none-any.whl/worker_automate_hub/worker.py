import asyncio
import os
from pathlib import Path

import pyfiglet
from rich.console import Console

from worker_automate_hub.api.client import (
    burnQueue,
    get_new_task,
    notify_is_alive,
    send_gchat_message,
)
from worker_automate_hub.config.settings import (
    load_env_config,
    load_worker_config,
)
from worker_automate_hub.tasks.task_definitions import is_uuid_in_tasks
from worker_automate_hub.tasks.task_executor import perform_task
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.updater import (
    get_installed_version,
    update_version_in_toml,
)

console = Console()


async def check_and_execute_tasks():
    while True:
        try:
            task = await get_new_task()
            worker_config = load_worker_config()
            if task is not None:
                processo_existe = await is_uuid_in_tasks(task["data"]['uuidProcesso'])
                if processo_existe:
                    await burnQueue(task["data"]["uuidFila"])
                    logger.info(f"Executando a task: {task['data']['nomProcesso']}")
                    await perform_task(task["data"])
                else:
                    log_message = f"O processo [{task["data"]['nomProcesso']}] não existe no Worker [{worker_config["NOME_ROBO"]}] e não foi removido da fila."
                    logger.error(log_message)
                    await send_gchat_message(log_message)
            else:
                err_msg = "newJob retornou None"
                logger.error(err_msg)
                console.print(err_msg, style="red")
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"Ocorreu um erro de execução: {e}")
            await asyncio.sleep(5)


async def notify_alive():
    env_config, _ = load_env_config()
    while True:
        try:
            logger.info("Notificando last alive...")
            await notify_is_alive()
            await asyncio.sleep(int(env_config["NOTIFY_ALIVE_INTERVAL"]))
        except Exception as e:
            logger.error(f"Erro ao notificar que está ativo: {e}")
            await asyncio.sleep(int(env_config["NOTIFY_ALIVE_INTERVAL"]))


async def main_process():
    current_dir = Path.cwd()
    toml_file_path = os.path.join(current_dir, 'settings.toml')
    atual_version = get_installed_version("worker-automate-hub")
    update_version_in_toml(toml_file_path, atual_version)
    worker_config = load_worker_config()
   
    custom_font = "slant"
    ascii_banner = pyfiglet.figlet_format(f"Worker", font=custom_font)
    os.system("cls")
    console.print(ascii_banner + f" versão: {atual_version}\n", style="bold blue")
    initial_msg = f"Worker em execução: {worker_config["NOME_ROBO"]}"
    logger.info(initial_msg)
    console.print(f"{initial_msg}\n", style="green")

    tasks = [check_and_execute_tasks(), notify_alive()]
    await asyncio.gather(*tasks)


def run_worker():
    try:
        while True:
            asyncio.run(main_process())
            break
    except asyncio.CancelledError:
        logger.info("Aplicação encerrada pelo usuário.")
