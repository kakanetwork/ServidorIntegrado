
# ============================================================================================================

''' IMPORTANDO BIBLIOTECAS NECESSÁRIAS PARA O FUNCIONAMENTO DO CÓDIGO '''

try:
    import socket, threading, os, sys, logging, logging.config
except:
    print(f'\nErro na Importação das Bibliotecas necessárias...{sys.exc_info()[0]}')  
    sys.exit()

# ============================================================================================================

''' DEFINIÇÃO DE ALGUMAS VARIAVEIS E DIRETÓRIOS '''

dir_atual = os.path.dirname(os.path.abspath(__file__))  # pegando a pasta atual
dir_arq =  os.path.abspath(__file__) 
dir_logconf = dir_atual + "\\log.ini"
dir_log = dir_atual + "\\log_server.log"
dir_pastdownload = dir_atual + '\\server_files'

# ============================================================================================================

''' CONFIGURAÇÃO DO LOG '''

try:
    logging.config.fileConfig(dir_logconf, defaults={'log_path': dir_log.replace('\\', '\\\\')}) # lendo o log.ini na pasta atual
    urllib3_logger = logging.getLogger('urllib3') 
    urllib3_logger.setLevel(logging.WARNING) # deixando o level dos logs da URLLIB3 em warning (motivo: espama muitos logs info por conta das requisições do telegram)
    loggerServer  = logging.getLogger('Server') # pegando os logger definidos na configuração (Server/BotTelegram e debug para fins de debug do código)
    loggerBot = logging.getLogger('BotTelegram')
    loggerDebug = logging.getLogger('Debug')
except:
    print(f'\nErro na Inicialização da Configuração do Log!\nVerifique se seu arquivo "log.ini" está devidamente Configurado... {sys.exc_info()[0]}\n')
    sys.exit()

# ============================================================================================================

''' VERIFICAÇÃO SE TODOS OS ARQUIVOS/PASTAS DE FUNÇÕES ESTÃO PRESENTES '''

def VERIFICATION_FUNCTIONS():
    dir_past = dir_atual + '\\Functions-and-Variables'
    sys.path.append(dir_past) # adicionando a pasta de funções na config de pesquisa de funções do sistema
    name_arqs = [
        'functions_bot.py',
        'functions_client.py',
        'functions_others.py',
        'functions_server.py',
        'functions_download.py',
        'variables.py',
        'rss.conf']
    try:
        functions_arq = os.listdir(dir_past) # listando arquivos da pasta onde está as funções para verificar se todos os arquivos necessários estão lá
    except FileNotFoundError: # para caso a pasta não exista
        loggerDebug.critical('A pasta "Functions and Variables" não foi encontrada, faça o download dela [com todas suas dependencias]!')
        sys.exit()
    except:
        loggerDebug.critical(f'Erro na Verificação dos arquivos da Pasta de Funções...{sys.exc_info()[0]}')  
        sys.exit() 
    else:
        for arquivos in name_arqs: 
            if arquivos not in functions_arq: # vendo qual o arquivo que falta
                loggerDebug.critical(f'O Arquivo "{arquivos}" nao este presente dentro da pasta "Functions and Variables" faca o download dele!')
                sys.exit()

VERIFICATION_FUNCTIONS()

# ============================================================================================================

''' APÓS REALIZAR VERIFICAÇÃO DOS ARQUIVOS, REALIZO O IMPORT DAS FUNÇÕES PRÓPRIAS '''

try:
    from variables import SERVER, PORT
    from functions_server import CLIENT_INTERACTION
    from functions_others import CREATE_PAST
    from functions_bot import START_BOT, NOTIFICATION_BOT
except SystemExit:
    sys.exit()
except:
    loggerDebug.critical(f'Alguma das Funcoes necessarias para o codigo nao foi encontrada!...{sys.exc_info()[0]}')
    sys.exit()

# ============================================================================================================

try: 

    ''' CRIAÇÃO THREAD BOT / CRIAÇÃO DO SERVER / CRIAÇÃO DE PASTA'''

    clients_connected = dict() # lista de clientes conectados (IP:PORTA)
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # conexão IPV4/TCP
    sock_tcp.bind((SERVER, PORT)) # atribuindo Porta e Ip
    CREATE_PAST(dir_atual + '\\server_files') # criando pasta onde sera guardado arquivos do server
    loggerServer.info(f'Servidor Iniciado: {SERVER} / {PORT}') # informando o inicio do servidor, seu IP/PORTA
    thread_bot = threading.Thread(target=START_BOT, args=(clients_connected, dir_log)) # adicionando a thread do bot (pois sem ela, eu não consegueria rodar o server e o bot ao mesmo tempo)
    thread_bot.start() # iniciando a thread do bot
    sock_tcp.listen() # deixando indefinido quantidade máxima de conexões

# ============================================================================================================

    ''' CONEXÃO DE CLIENTES / NOTIFICAÇÃO BOT / THREAD CLIENTE ''' 

    while True: 
        try:
            sock_client, info_client = sock_tcp.accept() # aceitando clientes 
            msg_connected = f"O Cliente de IP: {info_client[0]} | Na Porta: {info_client[1]} - Foi conectado com sucesso!" 
            loggerServer.info(msg_connected) # informando o cliente conectado
            NOTIFICATION_BOT(msg_connected) # enviando mensagem para o bot do cliente que se conectou [Questão pedida]
            clients_connected[info_client[1]] = [info_client[0], sock_client] # adicionando o cliente ao dicionario de clientes conectados (PORTA:IP,SOCKET)
            thread_client = threading.Thread(target=CLIENT_INTERACTION, args=(sock_client, info_client, clients_connected, dir_atual)) # adicionando uma thread para cada cliente
            thread_client.start() # iniciando a thread

# ============================================================================================================

            ''' EXCEÇÕES... ''' 

        except:
            loggerServer.critical(f'Erro na Inicialização da Thread...{sys.exc_info()[0]}')  
            sys.exit() 
            
except OSError as e: # exceção para quando a porta do servidor atual estiver ocupada
    if e.errno == 98:
        loggerServer.critical('A porta atual do servidor se encontra ocupada!')
        sys.exit()
except ConnectionAbortedError:
    loggerServer.warning('O Servidor foi desligado Abruptamente!')
    sys.exit()
except SystemExit: # SystemExit para fins de debug
    ...
except:
    loggerServer.critical(f'Erro na Inicialização do Server...{sys.exc_info()[0]}')  
    sys.exit() 

# ============================================================================================================