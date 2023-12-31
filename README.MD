
<h1 align="center">📌 Projeto Server-Client Local</h1>

<p align="center">
  <img src="http://img.shields.io/static/v1?label=License&message=MIT&color=fe428e&style=for-the-badge"/>

  <img src="http://img.shields.io/static/v1?label=Python&message=3.11.0&color=fe428e&style=for-the-badge&logo=python&logoColor=white"/>

   <img src="http://img.shields.io/static/v1?label=STATUS&message=FINALIZADO&color=fe428e&style=for-the-badge"/>
</p>

### Libs Utilizadas:
##### Padrões:
    - os, sys, time, logging.config, logging, socket, threading, ssl 
    subprocess, signal.
##### Terceiras:
    - requests, xml.etree.ElementTree e platform.

### Descrição do Funcionamento Servidor:
#### Pré-Execução: 
  - Tenha todas as bibliotecas citadas acima instaladas, para instalação utilize: <code>pip install name_lib </code>
  - Tenha todos os arquivos dessa pasta baixados seguindo a mesma estrutura, evite renomeamento de arquivos. Qualquer arquivo em falta constará no LOG do servidor.
  - Se for sua primeira execução do server, ele irá criar o arquivo "credentials.py" (dentro da pasta de funções) e pedirá para inserir sua API_KEY e seu ID_CHAT do telegram, após isso execute o server novamente!
#### Para Executar: <code>python launcher.py /start</code>, será inicializado o server na porta "5678", e ficará a espera de conexões.
  - Utilize: <code>python launcher.py /stop</code> para derrubar o server e desconectar todos os clientes.
  - A tentativa de /start com server já inicializado anteriormente não será bem sucedida da mesma que /stop também não, se não tiver iniciado.
  - Após inicialização alguns arquivos e pastas serão criados, a exclusão dos mesmos podem comprometer o funcionamento correto do código (Esses arquivos podem ser apagados após desligar o server).
#### Arquivos configuráveis:
##### O servidor possui alguns arquivos configuráveis para o seu uso personalizado, segue abaixo quais são e como configurar corretamente.
  - rss.conf: neste arquivo você pode inserir as URL's de feed RSS, que deseja utilizar para pesquisa, tenha ao menos 1 URL ativada para o funcionamento correto do código. Insira as URL completas, sem espaços extras, e no máximo uma por linha.
  - variables.py: esse arquivo guarda algumas variáveis importantes, mude apenas o necessário, como o Prompt de pergunta do cliente, Porta local do servidor e o número máximo de notícias do feed RSS a serem mostradas.
  Evite a alteração das outras variáveis!

### Descrição do Funcionamento Cliente:
#### Para Executar: <code>python cliente.py</code>, será executado o cliente conectando automaticamente ao servidor, o prompt será carregada e poderá executar qualquer uma das funções abaixo:
  - /l: Listar clientes conectados
  - /m:ip:porta:mensagem: Enviar mensagem para cliente específico [Informe IP:PORTA do cliente]
  - /b:mensagem: Enviar mensagem em Broadcast [Informe mensagem]
  - /h: Lista o seu histórico de comandos
  - /f: Lista os arquivos disponíveis para download local
  - /d:arquivo: Faz o download de um arquivo do servidor [Informe nome do arquivo]
  - /u:arquivo: Faz upload do arquivo para o Server [Informe nome do arquivo]
  - /w:url: Faz o download do arquivo de uma URL no banco do servidor [Informe uma URL]
  - /rss:palavra: Retorna Notícias com a palavra informada [Informe palavra-chave]
  - /?: Lista as opções disponíveis
  - /q: Desconectar do Servidor

### Descrição do Funcionamento Bot Telegram:
##### O servidor possui integração com a API do Bot Telegram, se seu bot foi configurado corretamente pelo Bot Father, sua API_KEY e ID_CHAT foram passados da forma correta, o servidor realizará toda a leitura e envio de dados.
  - /u: Ao ser digitado este comando pelo telegram o servidor irá informar a lista de clientes conectados (IP:PORTA).
  - /log: Esta comando irá te enviar pelo telegram remotamente o Log Atual/Completo do servidor.
  - Avisos de conexões: O servidor está configurado para enviar automaticamente uma mensagem de "aviso de conexão" para qualquer cliente que se conectar ao servidor.

<h2 align="center">👀 Mais informações</h2>
<p align="center">
    Para mais informações sobre os projetos presentes neste repositório ou para sugerir alterações e correções, entre em contato comigo pelo meu perfil do GitHub, Instagram ou Linkedin.
</p>
<div align="center">
    <a href="https://github.com/kakanetwork"><img src="https://img.shields.io/badge/-GitHub-4d080e?style=for-the-badge&color=141321&logo=github&logoColor=fe428e" alt="GitHub"></a>
    <a href="https://www.instagram.com/kaka_0206/"><img src="https://img.shields.io/badge/-Instagram-4d080e?style=for-the-badge&logo=instagram&color=141321&logoColor=fe428e" alt="Instagram"></a>
    <a href="https://https://www.linkedin.com/in/kalvinklein"><img src="https://img.shields.io/badge/-linkedin-4d080e?style=for-the-badge&logo=linkedin&color=141321&logoColor=fe428e" alt="Instagram"></a>
    
</div>

<code> - by kakanetwork </code>

