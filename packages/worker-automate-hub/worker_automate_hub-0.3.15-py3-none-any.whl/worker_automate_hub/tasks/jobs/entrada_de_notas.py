import asyncio
import warnings
import time
from datetime import datetime
import pyperclip
import re

import pyautogui
from rich.console import Console
from pywinauto.application import Application

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    find_target_position,
    kill_process,
    login_emsys,
    take_screenshot,
    take_target_position,
    type_text_into_field,
    select_model_capa,
    import_nfe,
    select_nfe,
    image_to_data
)
pyautogui.PAUSE = 0.5
console = Console()



async def entrada_de_notas(task):
    """
    Processo que relazia entrada de notas no ERP EMSys(Linx).

    """
    try:
        #Get config from BOF
        config = await get_config_by_name("login_emsys")
        console.print(task)
       
        #Seta config entrada na var nota para melhor entendimento
        nota = task['configEntrada']

        #Abre um novo emsys
        await kill_process("EMSys")
        app = Application(backend='win32').start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings("ignore", category=UserWarning, message="32-bit application should be automated using 32-bit Python")
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config['conConfiguracao'], app, task)

        if return_login['sucesso'] == True:
            type_text_into_field('Nota Fiscal de Entrada', app['TFrmMenuPrincipal']['Edit'], True, '50')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('enter')
            console.print(f"\nPesquisa: 'Nota Fiscal de Entrada' realizada com sucesso", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login["retorno"]}")
            console.print(f"\nError Message: {return_login["retorno"]}", style="bold red")
            return return_login
        
        time.sleep(10)
        #Procura campo documento
        model  = select_model_capa()
        if model['sucesso'] == True:
            console.log(model['retorno'], style='bold green')
        else:
            return {"sucesso": False, "retorno": f"{model['retorno']}"}

        #Clica em 'Importar-Nfe'
        imported_nfe  = import_nfe()
        if imported_nfe['sucesso'] == True:
            console.log(imported_nfe['retorno'], style='bold green')
        else:
            return {"sucesso": False, "retorno": f"{import_nfe['retorno']}"}

        #Seleciona 'Notas de outras empresas'
        nfe_select = select_nfe("Empresas")
        if nfe_select['sucesso'] == True:
            console.log(nfe_select['retorno'], style='bold green')
        else:
            return {"sucesso": False, "retorno": f"{nfe_select['retorno']}"}
        #Clica em  'OK' para selecionar
        pyautogui.click(970, 666)
        time.sleep(3)

        #Tela importa nota de outra empresa
        #Seleciona Empresa externa
        screenshot_path = take_screenshot()
        field = find_target_position(screenshot_path, "de", 30, 0, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Empresa'"}
        pyautogui.click(field)
        pyautogui.write(str(int(nota['cnpjFornecedor'][8:12])))
        pyautogui.hotkey('tab')

        #Digita datas de emissão
        field = find_target_position(screenshot_path, "emissão", 0, 40, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Data de emissão inicio'"}
        pyautogui.click(field)
        pyautogui.write(nota['dataEmissao'].replace('/', ''))

        field = find_target_position(screenshot_path, "a", 0, 40, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Data de emissão fim'"}
        pyautogui.click(field)
        pyautogui.write(nota['dataEmissao'].replace('/', ''))

        #Digita numero da nota
        field_num = find_target_position(screenshot_path, "Núm", 0, 60, 15)
        if field == None:
           return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo 'Núm Nota'"}
        pyautogui.click(field)
        pyautogui.write(nota['numeroNota'])

        #Clica em pesquisar
        field = find_target_position(screenshot_path, "pesquisar", 0 ,0, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o botão 'Pesquisar'"}
        pyautogui.click(field)
        time.sleep(120)
  
        #clica na nota
        pyautogui.click(791,483)
        time.sleep(2)

        #Clica em 'Importar'
        field = find_target_position(screenshot_path, "cancelar",0 ,100 , 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o botão importar"}
        pyautogui.click(field)
        
        time.sleep(10)

        #Identifica se ja foi importada
        screenshot_path = take_screenshot()
        field = find_target_position(screenshot_path, "falha" , 0, 0, 10)
        if field == None:
            ...
        else:
            console.log("Nota já lançada ou não encontrada.", style='bold green')
            return {"sucesso": False, "retorno": f"Nota já lançada ou não encontrada."}


        #Tela "Infromações para importação da Nota Fiscal Eletrônica"
        screenshot_path = take_screenshot()

        if nota['existeDespesa'] == 'Sim':
            #Digita natureza da operação
            pyautogui.hotkey('tab')
            pyautogui.write("1152")
            pyautogui.hotkey('tab')

            #Digita tipo despesa
            field = find_target_position(screenshot_path, "Despesa", 15, 40, 15)
            if field == None:
                return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo despesa"}
            pyautogui.click(field)
            pyautogui.write("291")
            pyautogui.hotkey("tab")

            #Marca "Manter Natureza de operação selecionada"
            pyautogui.click(963, 578)
            #Marca "Manter Calculo PIS/COFINS"
            pyautogui.click(705, 667)

        #Clica em ok
        pyautogui.click(1100, 730)
        time.sleep(60)

        #TODO fazer tratativa de "itens com ncm divergente" - PASSO 27.1 DA IT
        screenshot_path = take_screenshot()
        console.log("Procurando itens com ncm divergente", style='bold yellow')
        itens = find_target_position(screenshot_path, 'NCM', 0, 0, 10)
        if itens is not None:
            pyautogui.click(1000,568)
            console.log("Clicou em não nos itens com ncm divergente", style='bold yellow')
        else:
            console.log("0 Itens com ncm divergente", style='bold green')

        #TODO Itens não localizados - PASSO 27.2 DA IT
        #TODO trativa "Selecionar itens fornecedor" - PASSO 27.3 da it
        screenshot_path = take_screenshot()
        field = find_target_position(screenshot_path, "fornecedor", 15, 40, 15)
        if field is not None:
            pyautogui.click(field)
            screenshot_path = take_screenshot()
            img_data = image_to_data(screenshot_path)
            # for i in range(len(img_data['text'])):
                
        else:
            console.log("Não existe tela 'Selecionar itens fornecedor'", style='bold green')

        screenshot_path = take_screenshot()
        #Seleciona pagamento
        field = find_target_position(screenshot_path, "pagamento", 0, 0, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo de seleção de pagamento"}
        pyautogui.click(field)
        time.sleep(1)
        screenshot_path = take_screenshot()
        #Seleciona "Espécie de Caixa"
        field = find_target_position(screenshot_path, "Espécie", 0, 100, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo para selecionar espécie de caixa"}
        pyautogui.click(field)
        pyautogui.write("27")
        pyautogui.hotkey("enter")
    
        #Digita "Valor"
        field = find_target_position(screenshot_path, "Documento", 0, 200, 15)
        if field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo para digitar o valor"}
        pyautogui.doubleClick(field)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("del")
        pyautogui.write(nota['valorNota'])

        #Clica para lançar a nota
        pyautogui.click(594, 299)
        time.sleep(5)

        #Variação Maxima de custo
        pyautogui.click(1234, 633)

        #Quantidade de tempo alta devido o emsys ser lento
        time.sleep(120)

        screenshot_path = take_screenshot()
        message_nota = find_target_position(screenshot_path, "incluída", 0, 0, 15)
        if message_nota != None:
            pyautogui.click(960, 565)
            return {"sucesso": True, "retorno": f"Nota Lançada"}
        
        screenshot_path = take_screenshot()
        rateio_window = find_target_position(screenshot_path, "rateio", 0, 0, 15)
        if rateio_window != None:
            pyautogui.click(rateio_window)
            screenshot_path = take_screenshot()
            
            #Clica em Selecionar todos
            field = find_target_position(screenshot_path, "todos", 0, 0, 15)
            if field == None:
                return {"sucesso": False, "retorno": f"Campo 'Selecionar Todos' não encontrado"}
            pyautogui.click(field)
            time.sleep(2)
            
            #Digita "Centro" 1000 + filialEmpresaOrigem
            field = find_target_position(screenshot_path, "centro", 0, 85, 15)
            if field == None:
                return {"sucesso": False, "retorno": f"Campo centro não localizado"}
            pyautogui.click(field)
            filial = 1000 + int(nota['filialEmpresaOrigem'])
            pyautogui.write(str(filial))
            pyautogui.hotkey("tab")

            #Marca "Aplicar rateio aos itens selecionados"
            pyautogui.hotkey("space")
            pyautogui.hotkey("tab")

            #Digita % Rateio
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("del")
            pyautogui.write("100")

            #Clica Incluir registro
            pyautogui.click(1161, 548)
            
            #Clica OK
            pyautogui.click(1200, 683)
            time.sleep(5)

        #Aviso CFOP
        screenshot_path = take_screenshot()
        field = None
        field = find_target_position(screenshot_path, "mesmo", 0, 0, 15)
        if field == None:
            console.print("Nota com CFOP correto")
        else:
            #Clica em OK
            pyautogui.click(1096, 603)
            #Clica em "Principal"
            field = find_target_position(screenshot_path, "Principal", 0, 0, 15)
            pyautogui.click(field)
            #Selecio no "Principal" a NOP correta
            field = find_target_position(screenshot_path, "Inscrição", 20, 0, 15)
            pyautogui.click(field)
            pyautogui.write("1152")
            #Clica para lançar a nota
            pyautogui.click(594, 299)

            #Clica novamente em ok na variação de custo      
            field = find_target_position(screenshot_path, "ultrapassam", 0, 0, 15)
            if field == None:
                console.print("Nota sem itens com variação de custo")
            else:
                pyautogui.click(1234, 633)
                
            
        screenshot_path = take_screenshot()
        message_nota = find_target_position(screenshot_path, "incluída", 0, 0, 15)
        if message_nota != None:
            pyautogui.click(960, 565)
            return {"sucesso": True, "retorno": f"Nota Lançada"}
        else:
            return {"sucesso": False, "retorno": f"Erro ao lançar nota"}

    except Exception as ex:
        observacao = f"Erro Processo Entrada de Notas: {str(ex)}"
        logger.error(observacao)
        console.print(observacao, style="bold red")
        return {"sucesso": False, "retorno": observacao}