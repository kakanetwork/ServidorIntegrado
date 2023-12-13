
import requests, sys, time, logging, os

dir_bot = os.path.dirname(os.path.abspath(__file__))
dir_credentials = dir_bot + '\\credentials.py'
loggerBot = logging.getLogger('BotTelegram')

# ============================================================================================================

''' VERIFICANDO A EXISTÊNCIA DA API_key PARA O TELEGRAM BOT'''

try:
    from credentials import API_KEY, ID_CHAT # verificando se a pasta com as credenciais existem 
except ModuleNotFoundError: 
    loggerBot.warning('Nao foi encontrado a sua API_key!')
    with open(dir_credentials, 'w') as arquive:
        arquive.write("API_KEY = 'YOUR_API_KEY'\nID_CHAT = YOUR_ID_CHAT_BOT")
    loggerBot.warning('O Arquivo "credentials.py" foi criado, insira a informacao da sua API_KEY / ID_CHAT dentro dele e reinicie o server!')
    sys.exit()
except: 
    loggerBot.critical(f'Erro na Aquisicao da API_KEY...{sys.exc_info()[0]}')  
    sys.exit()      

# ============================================================================================================

''' MONTAGEM DE VARIAVEL '''

url_req = f'https://api.telegram.org/bot{API_KEY}' # montagem variavel para requisição

# ============================================================================================================

''' FAZENDO A VALIDAÇÃO DA API_KEY '''

def VERIFICATION_KEY(): 
    try:
        verification_key = requests.get(url_req + '/getUpdates').json() # fazendo uma requisição
    except:
        loggerBot.critical(f'Erro na Verificacao da API_KEY...{sys.exc_info()[0]}')  
        sys.exit()
    else:
        if verification_key.get('ok'): # verificando se a requisição foi completa
            loggerBot.info(f'Sua API_KEY foi verificada com sucesso!')  
            pass # se for validada a api ira continuar normalmente o código
        else:
            loggerBot.critical(f'A chave: {API_KEY} Informada e invalida!')
            sys.exit(1)
   
VERIFICATION_KEY()

# ============================================================================================================

''' FUNÇÃO PARA NOTIFICAR O BOT A CADA CLIENTE CONECTADO '''

def NOTIFICATION_BOT(msg_connected):
    try:
        resposta = {'chat_id':ID_CHAT,'text':f'{msg_connected}'} # realizo a montagem da formatação para o chat com id especificado
        var = requests.post(url_req+'/sendMessage',data=resposta) # envio a mensagem via requests.post
    except:
        loggerBot.error(f'Erro no envio da mensagem de [Cliente Conectado] para o Bot...{sys.exc_info()[0]}')  
        sys.exit()

# ============================================================================================================

''' FUNÇÃO PARA LISTAR OS CLIENTES CONECTADOS AO BOT '''

def LIST_CLIENTS_BOT(clients_connected):
    try:
        num = 0
        if len(clients_connected) > 0: # verifica se existe algum cliente conectado
            msg_list = "Os clientes conectados são:\n" # formatação mensagem
            for chave, valor in clients_connected.items(): # pego cada cliente conectado (ip/porta) do dicionário já criado
                ip = valor[0] # Armazenamento Temporário 
                num+=1 # formatação numeração cliente
                msg_list += f"\nCLIENTE {num}\nIP: {ip}\nPORTA: {chave}\n\n" # formatação listagem clientes (lembrando que chave=porta e valor[0]=ip
        else: # se não existir ele informa para o chat que não possui nenhum conectado
            msg_list = "O Servidor não possui nenhum cliente conectado!"
        resposta = {'chat_id':ID_CHAT,'text':f'{msg_list}'} # realizo a montagem da formatação para o chat com id especificado
        var = requests.post(url_req+'/sendMessage',data=resposta) # envio a mensagem via requests.post
    except:
        loggerBot.error(f'Erro no momento de Listar os Clientes Conectados...{sys.exc_info()[0]}')  
        sys.exit() 

# ============================================================================================================

''' LISTANDO O LOG PARA O BOT DO TELEGRAM '''

def LOG_BOT(dir_log):
    try:
        file_name = 'log-server.txt'
        with open(dir_log, 'rb') as arquive: 
            log = arquive.read()    
        var = requests.post(url_req+'/sendDocument', data={'chat_id': ID_CHAT}, files={'document': (file_name, log)}) # realizo envio do Log como documento
    except:
        loggerBot.error(f'Erro no momento de listar o Log para o Bot do Telegram...{sys.exc_info()}')  
        sys.exit() 

# ============================================================================================================

''' INFORMANDO PARA DIGITAR UM COMANDO VÁLIDO '''

def INVALID():
    try:
        msg_invalid = "\nInforme um comando válido!\n\n/u -> Listagem de Clientes Conectados\n/log -> Listagem do Log atual do servidor\n"
        msg_invalid += "\nBy: https://github.com/kakanetwork"
        resposta = {'chat_id':ID_CHAT,'text':f'{msg_invalid}'} # faço o envio
        var = requests.post(url_req+'/sendMessage',data=resposta) 
    except:
        loggerBot.error(f'Erro no momento de Informar para digitar um comando válido...{sys.exc_info()[0]}')  
        sys.exit() 

# ============================================================================================================

''' FUNÇÃO PARA RECEBER MENSAGENS/COMANDOS DA CONVERSA COM O BOT '''

def START_BOT(clients_connected, dir_log):
    try:
        id_message = None # defino o id da mensagem como NONE, usado mais a frente
        while True: # while True para ficar "ouvindo" o chat
            # faço o get com o parametro offset = id_message, que inicialmente é NONE, transformo em .json e pego apenas oque tem dentro da variavel "RESULT"
            # isso me retorna todas as últimas mensagens do chat e seus parametros (ex: id da mensagem, pelo ID eu consigo identificar a última mensagem)
            chat = requests.get(url_req + '/getUpdates', params={'offset': id_message}).json().get('result', [])
            if len(chat) == 0: # verificando se o chat tá vazio, se estiver ele dá sleep de 1s, e volta pro while para não gastar processamento extra
                time.sleep(1)
                continue
            for message in chat: # pego cada mensagem das últimas mensagens
                if 'message' in message and 'text' in message['message']: # verifico se a chave 'message' e 'text' estão presentes
                    command = message['message']['text'] # pego o texto da mensagem
                    if command == '/u' : # verifico se o que foi digitado = /u
                        loggerBot.info('Foi pedido para Listar os Clientes Conectados!')
                        LIST_CLIENTS_BOT(clients_connected) # se sim, ativo a função de listagem dos clientes conectados
                    elif command == '/log':
                        loggerBot.info('Foi pedido para Listar o Log Atual!')
                        LOG_BOT(dir_log) # se sim, ativo a função de listagem do log
                    else:
                        INVALID()
                id_message= message['update_id'] + 1 # aqui eu defino o id message (pego ele dentro do .json), e jogo +1 pois funciona como um OFFSET
                # onde a cada mensagem, o seu id vai ser +1 em relação ao anterior
    except:
        loggerBot.error(f'Erro no momento de Ler as mensagens do Telegram...{sys.exc_info()}')  
        sys.exit() 

# ============================================================================================================

