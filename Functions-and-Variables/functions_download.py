
import socket, sys, ssl, logging, requests, os
from variables import *
from functions_others import *

loggerServer  = logging.getLogger('Server')

# ============================================================================================================

def REQUEST_RSS(url):
    try:
        response = requests.get(str(url))
        response.raise_for_status() #debug
        return response.text # retorna o resultado em texto/string
    except requests.exceptions.RequestException as e:
        print(f'Erro ao acessar a URL {url}: {e}')
        return None

# ============================================================================================================

''' REALIZANDO CONEXÃO HTTPS PARA O DOWNLOAD DE UMA URL [FUNÇÃO UTILIZADA NA FUNÇÃO DOWNLOAD_URL] '''

def SOCKET_HTTPS(localarquive, hostname):
    requisição = f'GET {localarquive} HTTP/1.1\r\nHOST: {hostname}\r\nConnection: close\r\n\r\n'    # define a requisição 
    context = ssl.create_default_context()      # criação do contexto SSL para conexão HTTPS
    context.check_hostname = False      # desativa a verificação do nome do host durante a autenticação SSL.
    context.verify_mode = ssl.CERT_NONE     # o certificado do servidor não será verificado
    socket_TCP_IPV4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     # criação do socket/ conexão com o server (IPV4/TCP)
    socket_conexão = context.wrap_socket(socket_TCP_IPV4, server_hostname=hostname)     # Envolve o socket criado anteriormente em uma conexão segura (wrap_socket)
    socket_conexão.connect((hostname, 443))     # estabelece a conexão
    socket_conexão.send(requisição.encode(UNICODE))     # enviando requisição pedida acima
    return socket_conexão # retornando conexão 

# ============================================================================================================

''' REALIZANDO CONEXÃO HTTP PARA O DOWNLOAD DE UMA URL [FUNÇÃO UTILIZADA NA FUNÇÃO DOWNLOAD_WEB] '''

def SOCKET_HTTP(localarquive, hostname):
    requisição = f'GET {localarquive} HTTP/1.1\r\nHOST: {hostname}\r\nConnection: close\r\n\r\n' # define a requisição 
    socket_conexão = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # criação do socket/ conexão com o server (IPV4/TCP)
    socket_conexão.connect((hostname, 80)) # estabelece a conexão
    socket_conexão.sendall(requisição.encode(UNICODE)) # enviando requisição pedida acima
    return socket_conexão # retornando conexão 

# ============================================================================================================

''' FUNÇÃO PARA REALIZAR O DOWNLOAD[PARTE BRUTA] DA URL FORNECIDA [CONTINUAÇÃO DA FUNÇÃO DOWNLOAD_URL] '''

def DOWNLOAD_WEB(socket_conexão, sock_client):
    data_ret = b'' 
    dados_recebidos = 0
    try:
        content_lenght = -1
        msg_download = f'\nDownload do Arquivo foi Iniciado!\n' # informo que o download foi iniciado
        MESSAGE_CLIENT(sock_client, msg_download)
        while True:   
            data = socket_conexão.recv(BUFFER)  # recebe a resposta em pedaços de 4096 bytes
            if not data: # se o pacote não possui nada, ele encerra o recebimento
                break
            data_ret += data 
            dados_recebidos += len(data)  # joga na variavel o quanto de bytes já foram recebidos
            position  = data_ret.find('\r\n\r\n'.encode()) # pegando posição de fim do Header
            headers   = data_ret[:position].decode('utf-8').lower()   # pegando o Header 
            try:
                content_lenght = CONTENT_LENGHT(headers)    # função para capturar o content length no header
                msg_download = f'\rBytes baixados: {dados_recebidos} / {content_lenght} bytes' # informando ao cliente o progresso
                MESSAGE_CLIENT(sock_client, msg_download)
            except: pass  # passando pois o content_lenght não é vital para o código [Motivo: Apenas estética, o download irá continuar da mesma forma]
        if content_lenght == -1:
            msg_size = 'Não foi possivel capturar o Content_Lenght...'
            loggerServer.warning(msg_size)
            MESSAGE_CLIENT(sock_client, msg_size) # criando um aviso para quando o content lenght não for pego 
        arquivo_dados = data_ret[position+4:]   # pegando os dados do arquivo
        content_type = CONTENT_TYPE(headers) # usando a função para pegar a extensão do arquivo pelo header
        msg_download = f'\n\nO Download do arquivo foi concluído!\n' # informando que o download foi concluído
        MESSAGE_CLIENT(sock_client, msg_download)
    except:
        loggerServer.error(f'Erro no recebimento dos dados do Download Web...{sys.exc_info()[0]}')  
        sys.exit()  
    socket_conexão.close() # fechando a conexão
    return arquivo_dados, content_type
    
# ============================================================================================================