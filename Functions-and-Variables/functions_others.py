import sys, os, logging
from variables import *

loggerServer  = logging.getLogger('Server')

# ============================================================================================================

''' FUNÇÃO PARA EVITAR A REPETIÇÃO DE CÓDIGO DE ENVIOS '''

def MESSAGE_CLIENT(sock, msg):
    try:
        sock.send(msg.encode(UNICODE))
    except:
        loggerServer.error(f'Erro ao enviar mensagem para o cliente...{sys.exc_info()[0]}')

# ============================================================================================================

''' REALIZA A PROCURA DO CONTENT_LENGHT DO ARQUIVO '''

def CONTENT_LENGHT (headers): # FUNÇÃO PARA RETIRAR O CONTENT-LENGTH DO HEADER DE UM ARQUIVO
    try:
        lines = headers.strip().split('\n')  # pego o header já decodificado e quebro ele em linhas
        for line in lines:
            if line.lower().startswith('content-length:'): # vasculho nessas linhas o content-length por meio do startswich que retorna True quando a palavra existir
                linha_length = int(line[16:]) # transforma em int e pega somente da posição 16 em diante
                return linha_length 
    except:
        loggerServer.warning(f'Erro na captura do Content-Lenght...{sys.exc_info()[0]}')

# ============================================================================================================

''' REALIZA A PROCURA DO CONTENT_TYPE DO ARQUIVO '''

def CONTENT_TYPE (headers): # FUNÇÃO PARA RETIRAR O CONTENT-TYPE DO HEADER DE UM ARQUIVO
    try:
        lines = headers.strip().split('\n') # pego o header já decodificado e quebro ele em linhas
        for line in lines:
            if line.lower().startswith('content-type:'): # vasculho nessas linhas o content-type por meio do startswich que retorna True quando a palavra existir
                extensao = line.strip().split('/')[1] # pego a linha do Content-type, retiro os espaços com strip() e quebro com split() onde tiver uma barra
                break
        html_verification = extensao.find(';') # EXCEÇÃO: quando a url é de um arquivo HTML, temos que fazer um filtro diferente para conseguir pegar a extensão
        if html_verification != -1:
            extensao = extensao.split(';')[0] # usamos split() para quebrar a extensão onde tiver ';' e pego o primeiro resultado 
                                              # formato content type HTML -> html; charset = utf-8
        return extensao
    except:
        loggerServer.error(f'Erro na captura do Content-Type...{sys.exc_info()[0]}')

# ============================================================================================================

''' REALIZA A QUEBRA DA URL SOMENTE NOS PARAMETROS QUE EU QUERO TER '''

def SPLIT_URL (url): # FUNÇÃO PARA QUEBRAR A URL E PEGAR INFORMAÇÕES IMPORTANTES
    url_fragmentada = url.split('/')
    hostname = url_fragmentada[2] # pegando o hostname (ex: freepik.com)
    localarquive = '/'+'/'.join(url_fragmentada[3:]) # pegando local do arquivo (ex: /image/ocean/iceocean.png)
    if '.' in url_fragmentada[-1]: # isso é para retirar a extensão que tiver anteriormente [Há qual as vezes não é a mesma contida no content-type]
        arquivename = url_fragmentada[-1].split('.')[0]
    else:
        arquivename = url_fragmentada[-1]
    if len(arquivename) >= 150: # mantendo o máximo do tamanho do arquivo em 150 caracteres [Ultrapassando esse valor ele não irá salvar o arquivo corretamente]
        arquivename = arquivename[0:150]
    caracteres_bloqueados = ['/', ':', '*', '?', '|', '<', '>', '"', '\\'] 
    for x in caracteres_bloqueados: # retirando caracteres que são proibidos de ter no nome de um arquivo, para salvar...
        arquivename = arquivename.replace(x, '') 
    protocol = url.split(':')[0] # pegando o protocolo da url
    return hostname, localarquive, arquivename, protocol

# ============================================================================================================

''' FUNÇÃO PARA REALIZAR PRINT ORGANIZADO [Apenas lado cliente] '''

def PRINT_DIV(dados):
    print('\n'+'-'*100)
    print(dados)
    print('-'*100)

# ============================================================================================================

''' FUNÇÃO PARA REALIZAR SPLIT DO COMANDO DO CLIENTE '''

def COMAND_SPLIT(msg): 
    try:
        msg_split = msg.split(':') # para casos de /b:mensagem (separar o comando do parametro/argumento )
    except:
        loggerServer.error(f'Erro no Split do Comand...{sys.exc_info()[0]}')  
    return msg_split

# ============================================================================================================

''' FUNÇÃO PARA REALIZAR A CRIAÇÃO DE UMA PASTA '''

def CREATE_PAST(name):
    try:
        os.makedirs(name, exist_ok=True) # utilizando makedirs para ter o parametro "exist_ok=true" para caso a pasta exista, não retorne erro!
    except:
        loggerServer.error(f'Erro na Criação da Pasta...{sys.exc_info()[0]}')  
        exit()      

# ============================================================================================================