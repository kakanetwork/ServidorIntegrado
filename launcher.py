
''' ESTE É O LAUNCHER DO SERVER, DESENVOLVIDO PARA INICIALIZA-LO EM BACKGROUND E DESLIGA-LO '''

# ============================================================================================================

import subprocess, sys, os, signal, platform

# ============================================================================================================

dir_atual = os.path.dirname(os.path.abspath(__file__)) 
dir_arq =  os.path.abspath(__file__) 
dir_pid = dir_atual + "\\pid.conf" # montando pasta
dir_vlog = dir_atual + '\\log.ini'
system = platform.system().lower() # pegando nome do sistema

# ============================================================================================================

if os.path.isfile(dir_vlog):
    pass
else:
    print('\nAntes da execução do server você precisa ter configurado o arquivo "log.ini"!\n')
    sys.exit()

# ============================================================================================================

''' FUNÇÃO PARA MATAR O PROCESSO '''

def KILL_PROCESS(pid):
    try:
        os.kill(int(pid), signal.SIGTERM) # uso o os.kill pela praticidade 
        os.remove(dir_pid) # removo o arquivo do pid
        print('\nO Server foi Desligado com sucesso!\n')
    except:
        os.remove(dir_pid) # para caso exista um pid, mas não seja válido, apago o arquivo também
        print('\nO Server ainda não foi Iniciado!\n')

# ============================================================================================================

''' FUNÇÃO PARA RODAR O PROCESSO EM BG '''

def PROCESS_RUNNER():
    try:

        if system == 'windows': # verificação de sistema 
            # utilizo o subprocess para executar ele em 2° plano e retornar o seu PID original
            process = subprocess.Popen(["pythonw", "app_server.py"], creationflags=subprocess.CREATE_NEW_CONSOLE).pid
        elif system == 'linux':
            process = subprocess.Popen(["python", "app_server.py", "&"], creationflags=subprocess.CREATE_NEW_CONSOLE).pid
        with open(dir_pid, "w") as file:
            file.write(str(process)) # após inicializar escrevo no arqivo do pid o número do pid 
        print(f'\nO Servidor foi iniciado em 2° Plano com sucesso!\nPID -> {process}\n')
    except:
        print(f'\nErro na hora de Rodar o Processo! {sys.exc_info()[0]}')
        sys.exit()

# ============================================================================================================

''' FUNÇÃO PARA VERIFICAÇÃO DO PID (SE EXISTE REALMENTE)'''

def VERIFICATION_PID(pid):
    try:
        if system == 'windows': # verificação de sistema
            # com o RUN ele me retorna detalhes do processos, logo se for False/None, o processo não existe
            process = subprocess.run(['Powershell', 'Get-Process', '-Id', pid], capture_output=True, text=True).stdout.strip()
        elif system == 'linux':
            process = subprocess.run(['ps', '-p', pid], capture_output=True, text=True).stdout.strip()
    except: 
        print(f'\nErro na hora de Verificar o PID! {sys.exc_info()[0]}')
    else:
        if process:
            print(f'\nO Server já está sendo rodado em 2° Plano com o PID: {pid}\n')
            sys.exit()
        else:
            PROCESS_RUNNER()

# ============================================================================================================

''' FUNÇÃO PARA LER O PID '''

def READ_PID(): 
    if os.path.isfile('pid.conf'): # verifico se o arquivo existe
        with open(dir_pid, 'r') as arquive:
            pid = arquive.readline().strip() # se existir ele ler e pega apenas a linha que interessa
        return pid
    else:
        return False

# ============================================================================================================

''' VERIFICAÇÃO PARA VSCODE/IDE'S '''

# nas IDE's executamos normalmente pelo "run/f5" para não ficar dando erro, ele vai executar o servidor 
try:
    args = sys.argv[1].lower()
except:
    print('\nlauncher.py < /start | /stop | /? >\n')
    sys.exit()
    
# ============================================================================================================

''' VERIFICANDO ARGUMENTOS DO SYS.ARGV E APENAS REDIRECIONANDO PARA O PROJETO! '''
if args == '/start':
    pid = READ_PID()
    if pid:
        VERIFICATION_PID(pid)
    else:
        PROCESS_RUNNER()
elif args == '/stop':
    pid = READ_PID()
    if pid:
        KILL_PROCESS(pid)
    else:
        print('\nO Server ainda não foi Iniciado!\n')
elif args == '/?':
    print('\n\nOpções:\npython launcher.py /start -> Para iniciar o servidor\npython launcher.py /stop -> Para desligar o servidor\n\n')
else:
    print('\nlauncher.py < /start | /stop | /? >\n')

# ============================================================================================================
