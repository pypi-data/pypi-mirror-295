import asyncio
import re
import time
import warnings
from datetime import datetime

import pyautogui
import pyperclip
from pywinauto.application import Application
from rich.console import Console

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    api_simplifica,
    extract_value,
    find_element_center,
    find_target_position,
    kill_process,
    login_emsys,
    select_model_pre_venda,
    take_screenshot,
    take_target_position,
    type_text_into_field,
    extract_nf_number
    )

console = Console()

ASSETS_BASE_PATH = 'assets/descartes_transferencias_images/'
ALMOXARIFADO_DEFAULT = "50"

async def descartes(task):
    try:
        #Inicializa variaveis
        pre_venda_message = None
        nota_fiscal = [None]
        log_msg = None
        valor_nota = None
        #Get config from BOF
        console.print("Obtendo configuração...\n")
        config = await get_config_by_name("Descartes_Emsys")
        itens = task['configEntrada']['itens']

        # Obtém a resolução da tela
        screen_width, screen_height = pyautogui.size()

        # Print da resolução
        console.print(f"Largura: {screen_width}, Altura: {screen_height}")

        # Abre um novo emsys        
        await kill_process("EMSys")
        app = Application(backend='win32').start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings("ignore", category=UserWarning, message="32-bit application should be automated using 32-bit Python")
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config['conConfiguracao'], app, task)
        
        if return_login['sucesso'] == True:
            console.print("Pesquisando por: Cadastro Pré Venda")
            type_text_into_field('Cadastro Pré Venda', app['TFrmMenuPrincipal']['Edit'], True, '50')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('enter')
            console.print(f"\nPesquisa: 'Cadastro Pre Venda' realizada com sucesso", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login["retorno"]}")
            console.print(f"\nError Message: {return_login["retorno"]}", style="bold red")
            return return_login

        time.sleep(7)

        #Preenche data de validade
        console.print("Preenchendo a data de validade...\n")
        screenshot_path = take_screenshot()
        target_pos = (961, 331) #find_target_position(screenshot_path, "Validade", 10, 0, 15) 
        if target_pos == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo de validade"}
        
        pyautogui.click(target_pos)
        pyautogui.write(f'{datetime.now().strftime("%d/%m/%Y")}', interval=0.1)
        pyautogui.press('tab')
        console.print(f"\nValidade Digitada: '{datetime.now().strftime("%d/%m/%Y")}'\n", style="bold green")
        time.sleep(1)
        
        #Condição da Pré-Venda 
        console.print("Selecionando a Condição da Pré-Venda\n")       
        condicao_field = find_target_position(screenshot_path, "Condição", 10, 0, 15) 
        if condicao_field == None:
            condicao_field = (1054, 330)
            
        pyautogui.click(condicao_field)
        time.sleep(1)
        pyautogui.write("A")
        time.sleep(1)
        pyautogui.press("down")
        pyautogui.press("enter")
        time.sleep(1)
        
        #Preenche o campo do cliente com o número da filial
        console.print("Preenchendo o campo do cliente com o número da filial...\n")
        cliente_field_position = await find_element_center(ASSETS_BASE_PATH + "field_cliente.png", (795, 354, 128, 50), 10)
        if cliente_field_position == None:
            cliente_field_position = (884, 384)  

        pyautogui.click(cliente_field_position)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("del")
        pyautogui.write(task['configEntrada']['filialEmpresaOrigem'])
        pyautogui.hotkey("tab")
        time.sleep(6)

        #Verifica se precisa selecionar endereço
        console.print("Verificando se precisa selecionar endereço...\n")
        screenshot_path = take_screenshot()
        window_seleciona_endereco_position = take_target_position(screenshot_path, "Endereço")
        if window_seleciona_endereco_position is not None:
            log_msg = f'Aviso para selecionar Endereço'
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            return {"sucesso": False, "retorno": log_msg}
        else:
            log_msg = "Sem Aviso de Seleção de Endereço"
            console.print(log_msg, style='bold green')
            logger.info(log_msg)
        
        # Clica em cancelar na Janela "Busca Representante"
        console.print("Cancelando a Busca Representante\n")
        screenshot_path = take_screenshot()
        window_busca_representante_position = take_target_position(screenshot_path, "Representante")
        if window_busca_representante_position is not None:
            button_cancelar_position = find_target_position(screenshot_path, "Cancelar", attempts=15)            
            pyautogui.click(button_cancelar_position)
        
        time.sleep(2)

        # Aviso "Deseja alterar a condição de pagamento informada no cadastro do cliente?"
        console.print("Verificando alerta de alteração de pagamento informada no cadastro do cliente...\n")
        screenshot_path = take_screenshot()
        payment_condition_warning_position = take_target_position(screenshot_path, "pagamento")
        if payment_condition_warning_position is not None:
            button_no_position = (999, 568) #find_target_position(screenshot_path, "No", attempts=15)            
            pyautogui.click(button_no_position)
            console.print(f"\nClicou 'No' Mensagem 'Deseja alterar a condição de pagamento informada no cadastro do cliente?'", style="bold green")
            time.sleep(6)
        else:
            log_msg = f"\nError Message: Aviso de condição de pagamento não encontrado"
            logger.info(log_msg)
            console.print(log_msg, style="bold red")
        time.sleep(3)

        #Seleciona 'Custo Médio' (Seleção do tipo de preço)
        console.print("Seleciona 'Custo Médio' (Seleção do tipo de preço)...\n")
        screenshot_path = take_screenshot()
        custo_medio_select_position = find_target_position(screenshot_path, "Médio", attempts=15)

        if custo_medio_select_position == None:
            custo_medio_select_position = (851, 523)

        if custo_medio_select_position is not None:
            pyautogui.click(custo_medio_select_position)
            button_ok_position = (1042, 583) #find_target_position(screenshot_path, "OK", attempts=15)            
            pyautogui.click(button_ok_position)
            time.sleep(5)
            console.print(f"\nClicou OK 'Custo médio'", style="bold green")
        else:
            log_msg = f"\nError Message: Campo 'Custo Médio' não encontrado"
            logger.info(log_msg)
            console.print(log_msg, style="bold yellow")

        time.sleep(8)        

        #Clica em ok na mensagem "Existem Pré-Vendas em aberto para este cliente."
        console.print("Clica em ok na mensagem 'Existem Pré-Vendas em aberto para este cliente.'\n")
        screenshot_path = take_screenshot()
        existing_pre_venda_position = find_target_position(screenshot_path, "Existem", attempts=15)

        if existing_pre_venda_position == None:
            existing_pre_venda_position = await find_element_center(ASSETS_BASE_PATH + "existing_pre_venda.png", (831, 437, 247, 156), 15)

        if existing_pre_venda_position is not None:
            button_ok_position = (962, 562)
            pyautogui.click(button_ok_position)
            console.print(f"\nClicou OK 'Pre Venda Existente'", style="bold green")
            time.sleep(5)
        else:
            log_msg = f"\nError Message: Menssagem de prevenda existente não encontrada"
            logger.info(log_msg)
            console.print(log_msg, style="bold yellow")        

        #Define representante para "1"
        console.print("Definindo representante para '1'\n")
        screenshot_path = take_screenshot()
        field_representante_position = find_target_position(screenshot_path, "Representante", 0, 50, attempts=15)

        if field_representante_position == None:
            field_representante_position = await find_element_center(ASSETS_BASE_PATH + "field_representante.png", (679, 416, 214, 72), 15)
            if field_representante_position is not None:
                lista = list(field_representante_position)
                lista[0] += 50
                lista[1] += 1
                field_representante_position = tuple(lista)

        if field_representante_position is not None:
            pyautogui.doubleClick(field_representante_position)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("del")
            pyautogui.write('1')
            pyautogui.hotkey("tab")
        
        time.sleep(3)

        #Seleciona modelo de capa
        console.print("Selecionando o modelo de capa...")
        screenshot_path = take_screenshot()
        model_descarte_position = find_target_position(screenshot_path, "Modelo", 0, 100, attempts=15)

        if model_descarte_position == None:
            model_descarte_position = await find_element_center(ASSETS_BASE_PATH + "field_modelo_faturamento.png", (681, 489, 546, 96), 15)
            if model_descarte_position is not None:
                lista = list(model_descarte_position)
                lista[0] += 100
                model_descarte_position = tuple(lista)

        if model_descarte_position == None:
            model_descarte_position = (848, 527)

        if model_descarte_position is not None:
            pyautogui.click(model_descarte_position)
            pyautogui.click(1500, 800)
            pyautogui.write("B")
            pyautogui.hotkey("tab")
        else:
            log_msg = f'Campo Modelo na capa da nota não encontrado'
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            return {"sucesso": False, "retorno": log_msg}

        #Abre Menu itens
        console.print("Abrindo Menu Itens...\n")
        menu_itens = await find_element_center(ASSETS_BASE_PATH + "menu_itens.png", (526, 286, 152, 45), 10)

        if menu_itens == None:
            menu_itens = (570, 317)

        if menu_itens is not None:
            pyautogui.click(menu_itens)
        else:
            log_msg = f'Campo "Itens" no menu da pré-venda não encontrado'
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            return {"sucesso": False, "retorno": log_msg}

        time.sleep(2)

        #Loop de itens
        console.print("Inicio do loop de itens\n")
        for item in itens:
            screenshot_path = take_screenshot()
            #Clica no botão inclui para abrir a tela de item
            console.print("Clicando em Incluir...\n")
            button_incluir = (905, 573) #find_target_position(screenshot_path, "Incluir", 0, 0, attempts=15)
            if button_incluir is not None:
                pyautogui.click(button_incluir)
                console.print("\nClicou em 'Incluir'", style='bold green')            
            else:
                log_msg = f'Botão "Incluir" não encontrado'
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                return {"sucesso": False, "retorno": log_msg}
            time.sleep(3)
            
            # Digita Almoxarifado
            console.print("Preenchendo o campo de almoxarifado...\n")
            screenshot_path = take_screenshot()
            field_almoxarifado = (839, 313) #find_target_position(screenshot_path, "Almoxarifado",0, 129, 15)
            if field_almoxarifado is not None:
                pyautogui.doubleClick(field_almoxarifado)
                pyautogui.hotkey('del')
                pyautogui.write(task['configEntrada']['filialEmpresaOrigem'] + ALMOXARIFADO_DEFAULT)
                pyautogui.hotkey('tab')
                time.sleep(2)
                console.print(f"\nDigitou almoxarifado {task['configEntrada']['filialEmpresaOrigem'] + ALMOXARIFADO_DEFAULT}", style='bold green')            
            else:
                log_msg = f'Campo Almoxarifado não encontrado'
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                return {"sucesso": False, "retorno": log_msg}

            #Segue para o campo do item
            console.print("Preenchendo o campo do item...\n")
            field_item = (841, 339) #find_target_position(screenshot_path, "Item", 0, 130, 15)
            if field_item is not None:
                pyautogui.doubleClick(field_item)
                pyautogui.hotkey('del')
                pyautogui.write(item['codigoProduto'])
                pyautogui.hotkey('tab')
                time.sleep(2)
                console.print(f"\nDigitou item {item['codigoProduto']}", style='bold green')
            else:
                log_msg = f'Campo Item não encontrado.'
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                return {"sucesso": False, "retorno": log_msg}


            #Checa tela de pesquisa de item
            console.print("Verificando a existencia da tela de pesquisa de item...\n")
            screenshot_path = take_screenshot()
            window_pesquisa_item = await find_element_center(ASSETS_BASE_PATH + "window_pesquisa_item.png", (488, 226, 352, 175), 10)
            console.print(f"Produto {item['codigoProduto']} encontrado", style="bold green")
            logger.info(f"Produto {item['codigoProduto']} encontrado")

            if window_pesquisa_item is not None:
                observacao = f"Item {item['codigoProduto']} não encontrado, verificar cadastro"
                console.print(f"{observacao}", style="bold green")
                logger.info(f"{observacao}")
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", observacao, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                return {"sucesso": False, "retorno": observacao}
                
            #Checa se existe alerta de item sem preço, se existir retorna erro(simplifica e bof)
            console.print("Verificando se existe alerta de item sem preço, se existir retorna erro(simplifica e bof)...\n")
            warning_price = await find_element_center(ASSETS_BASE_PATH + "warning_item_price.png",  (824, 426, 255, 191), 10)
            if warning_price is not None:
                observacao = f"Item {item['codigoProduto']} não possui preço, verificar erro de estoque ou de bloqueio."
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", observacao, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                return {"sucesso": False, "retorno": observacao}
            
            screenshot_path = take_screenshot()
            
            time.sleep(2)

            #Seleciona o Saldo Disponivel e verifica se ah possibilidade do descarte
            console.print("Selecionando o Saldo Disponivel e verificando se há possibilidade do descarte...\n")
            screenshot_path = take_screenshot()
            field_saldo_disponivel = (916, 606) #find_target_position(screenshot_path + "Saldo", 20, 0, 10)
            if field_saldo_disponivel is not None:
                pyautogui.doubleClick(field_saldo_disponivel)
                time.sleep(1)
                pyautogui.doubleClick(field_saldo_disponivel)
                time.sleep(1)
                pyautogui.doubleClick(field_saldo_disponivel)
                time.sleep(1)
                pyautogui.hotkey('ctrl', 'c')
                amount_avaliable= ''
                amount_avaliable = pyperclip.paste()
                console.print(f"Saldo Disponivel: '{amount_avaliable}'", style="bold green")

                #Verifica se o saldo disponivel é valido para descartar
                if int(amount_avaliable) > 0 and int(amount_avaliable) >= int(item['qtd']): 
                    field_quantidade = (1047, 606) #find_target_position(screenshot_path, "Quantidade", 20, 0, 15)
                    pyautogui.doubleClick(field_quantidade)
                    pyautogui.hotkey('del')
                    pyautogui.write(str(item['qtd']))
                    pyautogui.hotkey('tab')
                    time.sleep(2)
                else:
                    log_msg = f"Saldo disponivel: '{amount_avaliable}' é menor que '{item['qtd']}' o valor que deveria ser descartado. Item: '{item['codigoProduto']}'"
                    await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                    console.print(log_msg, style="bold red")
                    return {"sucesso": False, "retorno": log_msg}

            #Clica em incluir para adicionar o item na nota
            console.print("Clicando em incluir para adicionar o item na nota...\n")
            button_incluir_item = (1007, 745) #find_target_position(screenshot_path, "Inlcuir", 0, 0, 15)
            if button_incluir_item is not None:
                pyautogui.click(button_incluir_item)
                time.sleep(2)
            else:
                log_msg = f"Botao 'Incluir' item não encontrado"
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                console.print(log_msg, style="bold red")
                return {"sucesso": False, "retorno": log_msg}
            
            #Clica em cancelar para fechar a tela e abrir novamente caso houver mais itens
            console.print("Clicando em cancelar para fechar a tela e abrir novamente caso houver mais itens...\n")
            button_cancela_item = (1194, 745) #find_target_position(screenshot_path, "Cancela", 0, 0, 15)
            if button_cancela_item is not None:
                pyautogui.click(button_cancela_item)
                time.sleep(2)
            else:
                log_msg = f"Botao cancelar para fechar a tela do item nao encontrado"
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                console.print(log_msg, style="bold red")
                return {"sucesso": False, "retorno": log_msg}
            
        time.sleep(2)

        #Clica no botão "+" no canto superior esquerdo para lançar a pre-venda
        console.print("Clica no botão '+' no canto superior esquerdo para lançar a pre-venda")
        #Precisa manter por imagem pois não tem texto
        button_lanca_pre_venda = await find_element_center(ASSETS_BASE_PATH + "button_lanca_prevenda.png", (490, 204, 192, 207), 15)
        if button_lanca_pre_venda is not None:
            pyautogui.click(button_lanca_pre_venda.x, button_lanca_pre_venda.y)
            console.print("\nLançou Pré-Venda", style="bold green")
        else:
            log_msg = f"Botao lança pre-venda nao encontrado"
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            console.print(log_msg, style="bold red")
            return {"sucesso": False, "retorno": log_msg}
        
        time.sleep(5)

        screenshot_path = take_screenshot()

       #Verifica mensagem de "Pré-Venda incluida com número: xxxxx"
        console.print("Verificando mensagem de 'Pré-Venda incluida com número: xxxxx'...\n")
        included_pre_venda = find_target_position(screenshot_path, "incluída", attempts=15)
        if included_pre_venda is not None:
            #Clica no centro da mensagem e copia o texto para pegar o numero da pre-venda
            pyautogui.click(included_pre_venda)
            pyautogui.hotkey("ctrl", "c")
            pre_venda_message = pyperclip.paste()
            pre_venda_message = re.findall(r'\d+-\d+', pre_venda_message)
            console.print(f"Numero pré-venda: '{pre_venda_message[0]}'",style='bold green')
            #Clica no ok da mensagem
            button_ok = (1064, 604) #find_target_position(screenshot_path, "Ok", 15)
            pyautogui.click(button_ok)
        else:
            log_msg = f"Não achou mensagem Pré-Venda incluida."
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            console.print(log_msg, style="bold red")
            return {"sucesso": False, "retorno": log_msg}
        
        screenshot_path = take_screenshot()

        #Message 'Deseja pesquisar pré-venda?'
        console.print("Verificando a existencia da mensagem: 'Deseja pesquisar pré-venda?'...\n")
        message_prevenda = take_target_position(screenshot_path, "Deseja")
        if message_prevenda is not None:
            button_yes = find_target_position(screenshot_path, "Yes", attempts=15)
            pyautogui.click(button_yes)
        else:
            log_msg = f"Mensagem 'Deseja pesquisar pré-venda?' não encontrada."
            console.print(log_msg, style="bold yellow")
        
        screenshot_path = take_screenshot()
        #Confirma pré-venda
        #Pode não precisar em descartes, mas em trânsferencias é obrigatório
        console.print("Confirmando a Pre-Venda...\n")
        button_confirma_transferencia = take_target_position(screenshot_path, "confirma")
        if button_confirma_transferencia is not None:
            pyautogui.click(button_confirma_transferencia)
            console.log("Confirmou transferencia", style="bold green")
        else:
            log_msg = f"Botao 'Confirma' não encontrado"
            console.print(log_msg, style="bold yellow")
        
        pyautogui.moveTo(1200, 300)

        console.print("Verificando a mensagem: Confirmar transferencia...\n")
        screenshot_path = take_screenshot()
        message_confirma_transferencia = take_target_position(screenshot_path, "confirmar")
        if message_confirma_transferencia is not None:
            #clica em sim na mensagem
            button_yes= find_target_position(screenshot_path, "Yes", attempts=15)
            pyautogui.click(button_yes)
            console.log("Cliclou em 'Sim' para cofirmar a pré-venda", style='bold green')
            pyautogui.moveTo(1200, 300)
            time.sleep(2)
            screenshot_path = take_screenshot()
            vencimento_message_primeira_parcela = take_target_position(screenshot_path, "vencimento")
            #TODO apareceu em dev apenas pode nao ser necesário em prod mantive por segurança
            #Pode nao aparecer na prod
            if vencimento_message_primeira_parcela is not None:
                button_yes = find_target_position(screenshot_path, "Yes", attempts=15)
                pyautogui.click(button_yes)
            time.sleep(2)
            screenshot_path = take_screenshot()
            #Clica no OK 'Pre-Venda incluida com sucesso'
            button_ok = find_target_position(screenshot_path, "Ok", attempts=15)
            pyautogui.click(button_ok)
            console.log("Cliclou em 'OK' para pré-venda confirmada com sucesso", style='bold green')
        else:
            log_msg = f"Mensagem 'Deseja realmente confirmar esta pré-venda?' não encontrada."
            console.print(log_msg, style="bold yellow")

        pyautogui.moveTo(1000, 500)

        #Clica em Faturar
        console.print("Clicando em Faturar...\n", style='bold green')
        button_faturar = (1313, 395) #find_target_position(screenshot_path, "Faturar", attempts=15)
        if button_faturar is not None:
            time.sleep(2)
            pyautogui.click(button_faturar)
            console.print(f"Clicou em: 'Faturar'",style='bold green')
        else:
            log_msg = f"Não encontrou botão faturar"
            console.print(log_msg, style="bold yellow")
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            return {"sucesso": False, "retorno": f'{log_msg}'}
         
        time.sleep(10)

        #Verifica se existe a mensagem de recalcular parcelas
        console.print("Verificando se existe a mensagem de recalcular parcelas...\n", style='bold green')
        button_no = (999, 560)
        pyautogui.click(button_no)
        console.print("Clicou em 'Não' para recalcular parcelas\n", style='bold green')
       
        time.sleep(15)

         #Seleciona Modelo
        console.log("Selecionando o modelo...\n", style='bold green')
        retorno = await select_model_pre_venda("077", (874,267))
        if retorno == True:
            console.log('Modelo selecionado com sucesso', style='bold green')
        else:
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal[0], valor_nota)
            return {"sucesso": False, "retorno": retorno['retorno']}
        
        time.sleep(3)

        #Extrai total da Nota
        console.log("Obtendo o total da Nota...\n", style='bold green')
        valor_nota = await extract_value()
        if valor_nota:
            console.print(f"\nValor NF: '{valor_nota}'",style='bold green')
        else:
            console.print(f"Valor não extraído", style="bold yellow")

        #Clicar no botao "OK" com um certo verde
        console.print("Clicando no OK...\n", style='bold green')
        screenshot_path = take_screenshot()
        button_verde = (1180, 822) #find_target_position(screenshot_path, "Ok", attempts=15)
        if button_verde is not None:
            pyautogui.click(button_verde)
        else:
            log_msg = f"Não conseguiu achar botão 'OK'"
            console.print(log_msg)
            logger.info(log_msg)
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            return {"sucesso": False, "retorno": log_msg}
    
        time.sleep(5)

        #Aviso "Deseja faturar pré-venda?"
        console.print("Verificando a mensagem: 'Deseja faturar pré-venda?'...\n")
        screenshot_path = take_screenshot()
        faturar_pre_venda = find_target_position(screenshot_path, "faturar", attempts=15)
        if faturar_pre_venda is not None:
            button_yes = (918, 561) #find_target_position(screenshot_path, "yes", attempts=15)
            pyautogui.click(button_yes)
        else:
            log_msg = {
            "numero_pre_venda": pre_venda_message[0],
            "numero_nota": ''
            }
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal[0], valor_nota)
            return {"sucesso": False, "retorno": "Falha ao cliclar em: 'SIM' no aviso: 'Deseja realmente faturar esta Pré-Venda ?'"}

        time.sleep(10)

        #Mensagem de nota fiscal gerada com número
        console.log("Extraindo numero da nota fiscal", style='bold green')
        nota_fiscal = await extract_nf_number()
        console.print(f"\nNumero NF: '{nota_fiscal}'",style='bold green')

        time.sleep(15)

        #Transmitir a nota
        console.print("Transmitindo a nota...\n", style='bold green')
        pyautogui.click(875, 596)
        logger.info("\nNota Transmitida")
        console.print("\nNota Transmitida", style="bold green")

        time.sleep(120)

        #Fechar transmitir nota
        console.print("Fechando a transmissão da nota...\n")
        #Clica em ok "processo finalizado"
        pyautogui.click(957, 556)

        #Clica em  fechar
        pyautogui.click(1200, 667)
                
        log_msg = {
        "numero_pre_venda": pre_venda_message[0],
        "numero_nota": nota_fiscal[0],
        "valor_nota": valor_nota
        }
        await api_simplifica(task['configEntrada']['urlRetorno'], "SUCESSO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal[0], valor_nota)
        return {"sucesso": True, "retorno": log_msg}
 
    except Exception as ex:
        log_msg = f"Erro Processo Descartes: {ex}"
        logger.error(log_msg)
        console.print(log_msg, style="bold red")
        await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal[0], valor_nota)
        return {"sucesso": False, "retorno": log_msg}
    