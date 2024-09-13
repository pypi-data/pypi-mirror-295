import asyncio
import math
import os
import re
import subprocess
import time
import warnings
from pathlib import Path

import aiohttp
import cv2
import psutil
import pyautogui
import pyperclip
from PIL import Image, ImageEnhance, ImageFilter
from prompt_toolkit.shortcuts import checkboxlist_dialog, radiolist_dialog
from pytesseract import Output, pytesseract
from rich.console import Console
from worker_automate_hub.config.settings import load_worker_config
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.updater import get_installed_version

console = Console()


async def get_system_info():
    worker_config = load_worker_config()
    max_cpu = psutil.cpu_percent(interval=10.0)
    cpu_percent = psutil.cpu_percent(interval=1.0)
    memory_info = psutil.virtual_memory()

    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "maxCpu": f"{max_cpu}",
        "maxMem": f"{memory_info.total / (1024 ** 3):.2f}",
        "usoCpu": f"{cpu_percent}",
        "usoMem": f"{memory_info.used / (1024 ** 3):.2f}",
        "situacao": "{'status': 'em desenvolvimento'}",
    }


async def get_new_task_info():
    worker_config = load_worker_config()
    atual_version = get_installed_version("worker-automate-hub")
    return {
        "uuidRobo": worker_config["UUID_ROBO"],
        "versao": atual_version,
    }


def multiselect_prompt(options, title="Select options"):
    result = checkboxlist_dialog(
        values=[(option, option) for option in options],
        title=title,
        text="Use space to select multiple options.\nPress Enter to confirm your selection.",
    ).run()

    if result is None:
        console.print("[red]No options selected.[/red]")

async def kill_process(process_name: str):
    try:
        # Obtenha o nome do usuário atual
        current_user = os.getlogin()

        # Liste todos os processos do sistema
        result = await asyncio.create_subprocess_shell(
            f'tasklist /FI "USERNAME eq {current_user}" /FO CSV /NH',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            err_msg = f"Erro ao listar processos: {stderr.decode().strip()}"
            logger.error(err_msg)
            console.print(err_msg, style="bold red")
            return

        if stdout:
            lines = stdout.decode().strip().split("\n")
            for line in lines:
                # Verifique se o processo atual corresponde ao nome do processo
                if process_name in line:
                    try:
                        # O PID(Process ID) é a segunda coluna na saída do tasklist
                        pid = int(line.split(",")[1].strip('"'))
                        await asyncio.create_subprocess_exec(
                            "taskkill", "/PID", str(pid), "/F"
                        )
                        log_msg = f"Processo {process_name} (PID {pid}) finalizado."
                        logger.info(log_msg)
                        console.print(
                            f"\n{log_msg}\n",
                            style="bold green",
                        )
                    except Exception as ex:
                        err_msg = f"Erro ao tentar finalizar o processo {process_name} (PID {pid}): {ex}"
                        logger.error(err_msg)
                        console.print(
                            err_msg,
                            style="bold red",
                        )
        else:
            log_msg = f"Nenhum processo chamado {process_name} encontrado para o usuário {current_user}."
            logger.info(
                log_msg,
                None,
            )
            console.print(
                log_msg,
                style="bold yellow",
            )

    except Exception as e:
        err_msg = f"Erro ao tentar matar o processo: {e}"
        logger.error(err_msg)
        console.print(err_msg, style="bold red")


async def find_element_center(image_path, region_to_look, timeout):
    try:
        counter = 0
        confidence_value = 1.00
        grayscale_flag = False

        while counter <= timeout:
            try:
                element_center = pyautogui.locateCenterOnScreen(
                    image_path,
                    region=region_to_look,
                    confidence=confidence_value,
                    grayscale=grayscale_flag,
                )
            except Exception as ex:
                element_center = None
                console.print(
                    f"[{counter+1}] - Elemento não encontrado na posição: {region_to_look}"
                )

            if element_center:
                console.print(
                    f"[{counter+1}] - Elemento encontrado na posição: {region_to_look}\n",
                    style="green",
                )
                return element_center
            else:
                counter += 1

                if confidence_value > 0.81:
                    confidence_value -= 0.01

                if counter >= math.ceil(timeout / 2):
                    grayscale_flag = True

                await asyncio.sleep(1)

        return None
    except Exception as ex:
        console.print(
            f"{counter} - Buscando elemento na tela: {region_to_look}",
            style="bold yellow",
        )
        return None


def type_text_into_field(text, field, empty_before, chars_to_empty):
    try:
        if empty_before:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)

        field.type_keys(text, with_spaces=True)

        if str(field.texts()[0]) == text:
            return
        else:
            field.type_keys("{BACKSPACE " + chars_to_empty + "}", with_spaces=True)
            field.type_keys(text, with_spaces=True)

    except Exception as ex:
        logger.error("Erro em type_text_into_field: " + str(ex), None)
        console.print(f"Erro em type_text_into_field: {str(ex)}", style="bold red")


async def wait_element_ready_win(element, trys):
    max_trys = 0

    while max_trys < trys:
        try:
            if element.wait("exists", timeout=2):
                await asyncio.sleep(1)
                if element.wait("exists", timeout=2):
                    await asyncio.sleep(1)
                    if element.wait("enabled", timeout=2):
                        element.set_focus()
                        await asyncio.sleep(1)
                        if element.wait("enabled", timeout=1):
                            return True

        except Exception as ex:
            logger.error("wait_element_ready_win -> " + str(ex), None)
            console.print(
                f"Erro em wait_element_ready_win: {str(ex)}", style="bold red"
            )

        max_trys = max_trys + 1

    return False


async def login_emsys(config, app, task):

    from pywinauto.application import Application

    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
        message="32-bit application should be automated using 32-bit Python",
    )

    await asyncio.sleep(10)
    # Testa se existe alguma mensagem no Emsys
    console.print("Testando se existe alguma mensagem no Emsys...")
    window_message_login_emsys = await find_element_center(
        "assets/emsys/window_message_login_emsys.png", (560, 487, 1121, 746), 15
    )

    # Clica no "Não mostrar novamente" se existir
    console.print("Clicando no 'Não mostrar novamente' se existir...")
    if window_message_login_emsys:
        pyautogui.click(window_message_login_emsys.x, window_message_login_emsys.y)
        pyautogui.click(
            window_message_login_emsys.x + 383, window_message_login_emsys.y + 29
        )
        console.print("Mensagem de login encontrada e fechada.", style="bold green")

    # Ve se o Emsys esta aberto no login
    console.print("Verificando se o Emsys esta aberto no login...")
    image_emsys_login = await find_element_center(
        "assets/emsys/logo_emsys_login.png", (800, 200, 1400, 700), 60
    )

    if image_emsys_login:
        console.print("Aguardando a janela de login ficar pronta...")
        if await wait_element_ready_win(app["Login"]["Edit2"], 80):
            console.print("Procurando o icone disconect_database...")
            disconect_database = await find_element_center(
                "assets/emsys/disconect_database.png", (1123, 452, 1400, 578), 60
            )

            if disconect_database:
                # Realiza login no Emsys
                console.print("Realizando login no Emsys...")
                type_text_into_field(config["user"], app["Login"]["Edit2"], True, "50")
                pyautogui.press("tab")
                type_text_into_field(
                    config["pass"],
                    app["Login"]["Edit1"],
                    True,
                    "50",
                )
                pyautogui.press("enter")

                # Seleciona a filial do emsys
                console.print("Seleciona a filial do emsys...")
                selecao_filial = await find_element_center(
                    "assets/emsys/selecao_filial.png", (480, 590, 820, 740), 15
                )

                console.print(f"Selecao filial via imagem: {selecao_filial}")
                if selecao_filial == None:
                    screenshot_path = take_screenshot()
                    selecao_filial = find_target_position(
                        screenshot_path, "Grupo", 0, -50, attempts=15
                    )
                    console.print(f"Selecao filial localização de texto: {selecao_filial}")
                    if selecao_filial == None:
                        selecao_filial = (700, 639)
                        console.print(f"Selecao filial posição fixa: {selecao_filial}")

                    pyautogui.click(selecao_filial)
                    console.print(f"Escrevendo [{task["configEntrada"]["filialEmpresaOrigem"]}] no campo filial...")
                    pyautogui.write(task["configEntrada"]["filialEmpresaOrigem"])
                    

                else:                    
                    console.print(f"Escrevendo [{task["configEntrada"]["filialEmpresaOrigem"]}] no campo filial...")
                    type_text_into_field(
                        task["configEntrada"]["filialEmpresaOrigem"],
                        app["Seleção de Empresas"]["Edit"],
                        True,
                        "50",
                    )
                pyautogui.press("enter")

                button_logout = await find_element_center(
                    "assets/emsys/button_logout.png", (0, 0, 130, 150), 60
                )

                if button_logout:
                    console.print(
                        "Login realizado com sucesso.", style="bold green"
                    )
                    return {
                        "sucesso": True,
                        "retorno": "Logou com sucesso no emsys!",
                    }
        else:
            log_msg = "Elemento de login não está pronto."
            logger.info(log_msg)
            console.print(log_msg, style="bold red")
            return {"sucesso": False, "retorno": "Falha ao logar no EMSys!"}


async def api_simplifica(
    urlSimplifica: str,
    status: str,
    observacao: str,
    uuidsimplifica: str,
    numero_nota,
    valor_nota,
):

    data = {
        "uuid_simplifica": uuidsimplifica,
        "status": status,
        "numero_nota": numero_nota,
        "observacao": observacao,
        "valor_nota": valor_nota,
    }

    try:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            async with session.post(f"{urlSimplifica}", data=data) as response:
                data = await response.text()
                log_msg = f"\nSucesso ao enviar {data}\n para o simplifica"
                console.print(
                    log_msg,
                    style="bold green",
                )
                logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao comunicar com endpoint do Simplifica: {e}"
        console.print(f"\n{err_msg}\n", style="bold green")
        logger.info(err_msg)


def add_start_on_boot_to_registry():
    import winreg as reg

    try:
        # Caminho para a chave Run
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

        # Nome da chave
        key_name = "worker-startup"

        # Caminho para o executável no diretório atual
        directory_value = os.path.join(os.getcwd(), "worker-startup.bat")

        # Acessar a chave de registro
        registry_key = reg.OpenKey(
            reg.HKEY_CURRENT_USER, registry_path, 0, reg.KEY_SET_VALUE
        )

        # Adicionar ou modificar o valor
        reg.SetValueEx(registry_key, key_name, 0, reg.REG_SZ, directory_value)

        # Fechar a chave de registro
        reg.CloseKey(registry_key)

        log_msg = f"Chave {key_name} adicionada ao registro com sucesso com o valor '{directory_value}'!"
        console.print(
            f"\n{log_msg}\n",
            style="bold green",
        )
        logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao adicionar ao registro: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)


def create_worker_bat():
    try:
        # Caminho do diretório atual
        current_dir = os.getcwd()
        nome_arquivo = "worker-startup.bat"

        # Conteúdo do arquivo
        # cd %USERPROFILE%
        bat_content = f"""@echo off
cd {current_dir}        
start /min "" "worker" "run"
"""

        # Caminho completo para o arquivo
        bat_file_path = os.path.join(current_dir, nome_arquivo)

        # Escrevendo o conteúdo no arquivo
        with open(bat_file_path, "w") as file:
            file.write(bat_content.strip())

        log_msg = f"Arquivo {nome_arquivo} criado com sucesso em {bat_file_path}!"
        console.print(
            f"\n{log_msg}\n",
            style="bold green",
        )
        logger.info(log_msg)

    except Exception as e:
        err_msg = f"Erro ao criar o arquivo {nome_arquivo}: {e}"
        console.print(f"\n{err_msg}\n", style="bold red")
        logger.error(err_msg)


def take_screenshot() -> Path:   
    screenshot_path = Path.cwd() / "temp" / "screenshot.png"      
    screenshot_path.parent.mkdir(parents=True, exist_ok=True)    
    screenshot = pyautogui.screenshot()
    screenshot.save(screenshot_path)
    
    return screenshot_path


def preprocess_image(image_path):
    # Carregar a imagem
    image = cv2.imread(str(image_path))

    # Converter para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar threshold binário
    _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Remover ruído com medianBlur
    denoised_image = cv2.medianBlur(binary_image, 3)

    # Aumentar o contraste
    contrast_image = cv2.convertScaleAbs(denoised_image, alpha=1.5, beta=0)

    return contrast_image


def take_target_position(
    screenshot_path: Path, target_text: str, vertical=0, horizontal=0
) -> tuple | None:

    selected_image = Image.open(screenshot_path).convert("L")

    # Configurações do pytesseract
    # custom_config = r'--oem 3 --psm 6'

    # Extrair dados do texto usando pytesseract
    text_data = pytesseract.image_to_data(
        selected_image,
        output_type=pytesseract.Output.DICT,
        lang="por",  # , config=custom_config
    )

    # Identificar a posição do texto desejado
    field_center = None
    for i, text in enumerate(text_data["text"]):
        if len(text) > 0:
            if target_text.lower() in str(text).lower():
                x = text_data["left"][i]
                y = text_data["top"][i]
                w = text_data["width"][i]
                h = text_data["height"][i]
                # Centralizando nas coordenadas do campo
                field_center = (x + w // 2, y + h // 2)
                break

    # Aplicar as modificações de posição
    if field_center:
        field_center = (field_center[0] + horizontal, field_center[1] + vertical)

    return field_center


def find_target_position(
    screenshot_path: Path,
    target_text: str,
    vertical_pos: int = 0,
    horizontal_pos: int = 0,
    attempts: int = 5,
) -> tuple | None:
    # print("Dentro da função: ", screenshot_path)
    attempt = 0
    while attempt < attempts:
        target_pos = take_target_position(
            screenshot_path,
            target_text,
            vertical=vertical_pos,
            horizontal=horizontal_pos,
        )
        console.print(f"Tentativa {attempt + 1} - Posição: {target_pos}")
        attempt += 1
        time.sleep(1)
        if target_pos is not None:
            log_msg = f"Posição do campo [{target_text}] encontrada na tentativa [{attempt}], com valor de: {target_pos}"
            console.print(log_msg, style="green")
            logger.info(log_msg)
            break

    if target_pos == None:
        log_msg = f"Não foi possível encontrar o campo [{target_text}] em [{attempts}] tentativas!"
        console.print(log_msg, style="red")
        logger.error(log_msg)

    return target_pos

def select_model_capa():
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, "Documento", 0, 140, 15)
    if field == None:
        
        return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Documento'"}
    pyautogui.click(field)
    time.sleep(1)
    pyautogui.write("Nfe")
    pyautogui.hotkey("enter")
    #Procura o tipo de documento "NFe - NOTA FISCAL ELETRONICA PROPRIA - DANFE SERIE 077"
    while True:
        screenshot_path = take_screenshot()
        field = find_target_position(screenshot_path, "077", 0, 140, 5)
        if field is not None:
            break
        else:
            pyautogui.hotkey("down")
            time.sleep(2)

    return {"sucesso": True, "retorno": f"Modelo Selecionado"}

def import_nfe():
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, "Importar", 0, 0, 15) 
    if field == None:
        return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo de 'Importar NFe'"}
    pyautogui.click(field)
    time.sleep(8)
    return {"sucesso": True, "retorno": f"Clicou Importar nfe"}

def select_nfe(nfe_type):
    screenshot_path = take_screenshot()
    field = find_target_position(screenshot_path, nfe_type, 0 ,0, 15)
    if field == None:
        return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo de 'Notas de Outras Empresas'"}
    pyautogui.click(field)

    return {"sucesso": True, "retorno": f"Selecionou {nfe_type}"}

async def transmitir_nota(task, nota_fiscal, valor_nota):
    # screenshot_path = take_screenshot()
    # transmitir = find_target_position(screenshot_path, "transmitir", attempts=20)
    # if transmitir is not None:
    pyautogui.click(875, 596)
    logger.info("\nNota Transmitida")
    console.print("\nNota Transmitida", style="bold green")
    # else:
    #     log_msg = f'\nNota não Transmitida'
    #     logger.info(log_msg)
    #     console.print(log_msg ,style="bold red")
    #     await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
    #     return {"sucesso": False, "retorno": log_msg}

    time.sleep(7)

    #Fechar transmitir nota
    console.print("Fechando a transmissão da nota...\n")

    pyautogui.click(957, 556)

    time.sleep(15)
    screenshot_path = take_screenshot()
    transmitir_fechar = find_target_position(screenshot_path, "fechar", attempts=15)
    if transmitir_fechar is not None:
        pyautogui.click(transmitir_fechar)
        log_msg = f'Nota Transmitida com sucesso'
        logger.info(log_msg)
        console.print(log_msg, style="bold green")
    else:
        log_msg = f'Nota não transmitida'
        logger.info(log_msg)
        console.print(log_msg, style='bold red')
        await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
        return {"sucesso": False, "retorno": log_msg}


    return{'sucesso': True, 'retorno': "Nota transmitida com sucesso"}


async def select_model_pre_venda(text_to_find : str, mouse_pos : tuple, processo):
    #Procura se o campo de select ja possui a opção que você precisa selecionada
    screenshot = take_screenshot()
    field = find_target_position(screenshot, text_to_find, 0, 0, 5)
    if field:
        return True
    else:
        retorno = find_desired_model(mouse_pos, text_to_find, processo)
    
    if retorno:
        return retorno


async def extract_value():
    pyautogui.click(1304, 780)
    pyautogui.doubleClick(1304, 780)
    pyautogui.doubleClick(1304, 780)
    pyautogui.hotkey("ctrl", "c")
    console.log(f"Conteudo copiado: {pyperclip.paste()}", style='bold green')
    valor_nota = pyperclip.paste()
    # valor_nota = re.findall(r'\b\d{1,3}(?:\.\d{3})*,\d{2}\b', valor_nota)
    # print(valor_nota)
    return valor_nota


async def extract_nf_number():
    # screenshot_path = take_screenshot()
    # nota_fiscal_gerada = find_target_position(6395, "gerada", attempts=15)
    # pyautogui.click(nota_fiscal_gerada)
    pyautogui.click(965, 515)
    pyautogui.hotkey("ctrl", "c")
    nota_fiscal = pyperclip.paste()
    nota_fiscal = re.findall(r'\d+-?\d*', nota_fiscal)
    return nota_fiscal[0]

def find_desired_model(mouse_pos: tuple, text_to_find, processo):
    #Se não achou clica no campo modelo e sobe ate a primeira opção
    modelo_select_position = mouse_pos
    pyautogui.click(modelo_select_position)
    pyautogui.hotkey("tab")
    for _ in range(15):
        pyautogui.press('up')
    pyautogui.hotkey('enter')

    max_trys = 20
    trys = 0
    while trys < max_trys:
        pyautogui.hotkey('tab')
        screenshot = take_screenshot()
        console.log(f"Verificando se o modelo {text_to_find} existe.")
        field = find_target_position(screenshot, text_to_find, 0, 0, 3)
        if field:
            return {'sucesso': True, 'retorno': f'Campo {text_to_find} encontrado'}
        else:
            console.log(f"Modelo {text_to_find} inexistente. Seguindo para próximo.\n")
            console.log(f"Clicando em: {mouse_pos}\n")
            pyautogui.click(mouse_pos)
            if trys == 0 and processo.lower() == "descartes":
                pyautogui.press('down', presses=3)
                pyautogui.hotkey('enter')
                trys +=1
                continue
            elif trys == 0 and processo.lower() == "tranferencias":
                pyautogui.press('down', presses=1)
                pyautogui.hotkey('enter')
                trys +=1
                continue

            pyautogui.press('down')
            time.sleep(1)
            pyautogui.hotkey('enter')
            time.sleep(1)
            pyautogui.press('down')
            time.sleep(1)
            trys += 1


async def faturar_pre_venda(task, processo):
    #Clica em Faturar
        button_faturar = (1311, 396) #find_target_position(screenshot_path, "Faturar", attempts=15)
        time.sleep(2)
        pyautogui.click(button_faturar)
        console.print(f"Clicou em: 'Faturar'",style='bold green')

        time.sleep(10)

        #Aviso "Deseja faturar pré-venda?"
        button_yes = (918, 557) #find_target_position(screenshot_path, "yes", attempts=15)
        pyautogui.click(button_yes)

        time.sleep(10)

        #Verifica se existe a mensagem de recalcular parcelas
        screenshot_path = take_screenshot()
        message_recalcular = find_target_position(screenshot_path, "Recalcular", attempts=15)
        #Se existir clica em nao
        if message_recalcular is not None:
            button_no = (999, 560) #find_target_position(screenshot_path, "No", attempts=15)
            pyautogui.click(button_no)
            console.log("Cliclou em 'No' na mensagem de recalcular parcelas", style="bold green") 
        else:
            logger.info(f"Mensagem de para recalcular parcelas da pre-venda nao existe")
            console.print(f"Mensagem de para recalcular parcelas da pre-venda nao existe", style="bold yellow")
        
        time.sleep(8)

        #Seleciona Modelo
        console.log("Selecionando o modelo...\n", style='bold green')
        retorno = await select_model_pre_venda("077", (874,267), processo)
        if retorno == True:
            console.log('Modelo selecionado com sucesso', style='bold green')
        else:
            await api_simplifica(task['configEntrada']['urlRetorno'], "SUCESSO", retorno['retorno'], task['configEntrada']['uuidSimplifica'], None, None)
            return {"sucesso": False, "retorno": retorno['retorno']}

        #Extrai total da Nota
        console.log("Obtendo o total da Nota...\n", style='bold green')
        valor_nota = await extract_value()
        console.print(f"\nValor NF: '{valor_nota}'",style='bold green')

        #Clicar no botao "OK" com um certo verde
        button_verde = (1180, 822) #find_target_position(screenshot_path, "Ok", attempts=15)
        pyautogui.click(button_verde)
    
        time.sleep(5)

        #Clicar no botao "Yes" para "Deseja realmente faturar esta pre-venca?""
        button_yes = (920, 560) #find_target_position(screenshot_path, "Ok", attempts=15)
        pyautogui.click(button_yes)

        return True
