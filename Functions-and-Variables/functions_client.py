import socket, time, os, sys
from variables import *
from functions_others import *

# ============================================================================================================

''' FUNÇÃO PARA REALIZAR O ENVIO DE UPLOAD '''

def UPLOAD_SEND(name_arquive, dir_atual, sock_tcp):
    try:
        dir_arquivo = dir_atual + f'\\{name_arquive}' # pegando o nome do arquivo fornecido e montando caminho absoluto
        if not os.path.exists(dir_arquivo): # verificando se o arquivo fornecido existe [tem que está na mesma pasta do client.py]
            print(f'\nO Arquivo que você pediu "{name_arquive}" não existe no seu diretorio atual!\n') # informando caso não exista
            return
        size_arq = os.path.getsize(dir_arquivo) # existindo ele pega o tamanho do arquivo
        msg_local = f'/u:{size_arq}:{name_arquive}' # e faço o envio do comando, nome e tamanho do arquivo 
        sock_tcp.send(msg_local.encode(UNICODE)) # enviando antecipadamente nome e tamanho
        with open(dir_arquivo, 'rb') as arquive: # lendo o arquivo 
            while True:
                dados_arq = arquive.read(BUFFER)
                if not dados_arq:
                    break
                sock_tcp.send(dados_arq) # enviando o arquivo
    except FileNotFoundError:
        print(f'\nO Arquivo que você pediu "{name_arquive}" não existe no seu diretorio atual!\n')
    except IndexError: # para caso não seja repassado todos os argumentos de /d
        print(f"\nInforme todos os argumentos/parametros necessários para essa opção\n")
    except:
        print(f'\nErro no momento de realizar o UPLOAD [lado cliente]{sys.exc_info()}')

# ============================================================================================================

''' FUNÇÃO PARA REALIZAR O RECEBIMENTO DE DOWNLOADS '''

def DOWNLOAD_RECV(sock_tcp, size, name, dir_atual):
    try:
        os.makedirs('Downloads', exist_ok=True) # Criando a pasta onde vai armanezar (exist_ok=True para evitar erros de pasta já existente)
        local_arquive = dir_atual + f'\\Downloads\\{name}' # montando local do arquivo
        with open(local_arquive, 'wb') as arquivo: 
            bytes_recebidos = 0
            pct = 1
            print(f'\nGravando o arquivo: {name}\nTamanho: {size} bytes')
            while True:
                # Recebendo o conteúdo do servidor
                data_arquive = sock_tcp.recv(BUFFER) # recebendo o arquivo (buffer de 4096)
                if not data_arquive: break 
                arquivo.write(data_arquive) # gravando arquivo
                bytes_recebidos += len(data_arquive) 
                print(f'Pacote ({pct}) - Dados: {bytes_recebidos}/{size} bytes')
                if bytes_recebidos >= size: break
                pct += 1
        print('\nDownload Finalizado!\n')
    except FileNotFoundError:
        print(f'\nO Arquivo que você pediu "{name}" não existe no servidor!\nDê /f para consultar os arquivos existentes...\n')
        return
    except:
        print(f'Erro no recebimento do download Local...{sys.exc_info()}')

# ============================================================================================================

def CLOSE_SOCKET(sock_tcp):
    try:
        sock_tcp.close()
    except:
        None
    
# ============================================================================================================

''' FUNÇÃO PARA RECEBER RESPOSTAS DOS COMANDOS ENVIADOS '''

received_rss = False

def USER_RECV(sock_tcp, dir_atual):
    global received_rss # torno a variavel global para que as outras funções tenham acesso ao valor atualizado dela
    try:
        while True:
            retorno = sock_tcp.recv(512) # recebendo (obs: buffer baixo pois aqui só recebo mensagens, parte de download não é recebida aqui)
            if not retorno:  # Verificar se o retorno é vazio, indicando que o socket foi fechado pelo cliente (afim de evitar pequenos bugs)
                break
            msg = retorno.decode(UNICODE, errors='ignore') # erros=ignore utilizado para evitar bugs no RSS (alguns conteudos geram erros com o 'utf-8')
            if msg == '/q': 
                print("\nConexão encerrada.\n")
                break
            if msg == '/end_rss':  # Verifica se recebeu a flag de término das notícias 
                received_rss = False # se sim ele volta a considerar received_rss como false, liberando o input para uso
                continue
            if msg[:2] == '/d': # utilizando para quando é chamado a função de download (obs: essa primeira mensagem é uma flag exclusiva feita pelo server)
                # essa flag vai me enviar o tamanho e nome do arquivo (/d:size:name)
                info_arquive = COMAND_SPLIT(msg) # realizo a quebra para pegar separadamente
                size = int(info_arquive[1])
                name = info_arquive[2]
                DOWNLOAD_RECV(sock_tcp, size, name, dir_atual) # chamo a função de download
                continue
            print(msg) # printo o restante das mensagens/respostas recebidas
        CLOSE_SOCKET(sock_tcp)
    except ConnectionResetError:
        print(f'\n\nVocê foi desconectado do servidor!\n')
        sys.exit()
    except:
        print(f'\nErro na interacao com o servidor... {sys.exc_info()}')
        sys.exit()
       

# ============================================================================================================

''' FUNÇÃO PARA ENVIAR OS COMANDOS DO CLIENTE'''

def USER_SEND(sock_tcp, dir_atual):
    global received_rss # torno a variavel global para que as outras funções tenham acesso ao valor atualizado dela
    try:
        while True:
            if received_rss: # se caso received_rss for True, ele reinicia o laço até que seja False (isso impede que o imput seja acionado no meio do carregamento)
                continue
            msg = input(PROMPT) # input da mensagem
            if msg[:2] == '/u': # para ser acionada a função de Upload
                UPLOAD_SEND(msg[3:], dir_atual, sock_tcp)
                continue
            sock_tcp.send(msg.encode()) # para enviar a mensagem ao cliente
            if msg == '/q': # para ser desconectado de maneira correta
                print("\nConexão encerrada.\n")
                break
            if msg[:4] == '/rss': # se digitado /rss ele vai ativar o received_rss = True, para evitar inputs durante carregamento
                # foi necessário porconta do alto delay de carregamento das noticias a depender do RSS utilizado
                print('\nAs Notícias estão sendo carregadas, aguarde um momento...!')
                received_rss = True
            time.sleep(0.4) # time.sleep apenas para evitar pequenos bugs de input relacionados a velocidade do laço 
        CLOSE_SOCKET(sock_tcp)
    except ConnectionResetError:
        pass
    except:
        print(f'\nErro na interacao com o Usuário... {sys.exc_info()}')
        sys.exit()
        

# ============================================================================================================
