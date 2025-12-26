# Copilot Chat Conversation Export: Talon Voice on VSCode through light local client + API STT Azure

**User:** @felipecalado45
**Thread URL:** https://github.com/copilot/c/fae39b9e-b7d9-467a-9a5d-8c75ee882203

## @felipecalado45

Implementação do talon em máquina virtual na azure ou no colab

## Copilot

Quer que eu explique como instalar/rodar o Talon ou você quer que eu faça um passo-a-passo / script para implantar numa VM Azure ou numa sessão Colab? Antes de seguir, preciso de algumas clarificações — assim eu entrego exatamente o que você precisa:

1) Qual "Talon" você quer implementar?
   - Talon Voice (controle por voz / automação local — community config como knausj_talon)?  
   - Outro projeto chamado "talon" (dê link se for outro)?

2) Qual é o objetivo exato?
   - Controlar uma máquina remotamente por voz (usar Talon como cliente de controle)?
   - Treinar/rodar somente o modelo de reconhecimento (ASR) que o Talon usa?
   - Desenvolver/depurar configurações do Talon?
   - Outro objetivo?

3) Qual plataforma prefere e qual sistema operacional na VM?
   - Azure VM (Linux ou Windows)?
   - Google Colab?
   - Palavra-chave importante: Colab tem limitações fortes para Talon (explico abaixo).

4) Você tem:
   - Conta Azure com permissão para criar VMs / GPU?
   - Preferência por GUI remoto (RDP) ou só SSH?

Rápido resumo técnico e recomendações (útil mesmo se só quiser decidir):

- Colab: não é indicado para instalar Talon Voice. Talon precisa de acesso a microfone local, interfaces de entrada/controle (keyboard/mouse em nível do sistema) e, normalmente, acesso a uma sessão gráfica ou integração com o sistema host — Colab não fornece microfone local nem controle do host. Colab pode até rodar modelos de ASR (transcrição) para fins experimentais, mas não substitui o Talon por controle local.

- Azure VM: é viável, mas com ressalvas:
  - Em Windows VM (RDP) você pode redirecionar áudio do cliente para a VM e rodar Talon, porém Talon costuma esperar controle do próprio sistema onde o usuário interage — usar Talon em VM para controlar o host remoto funciona, mas para controlar seu computador local é mais complexo.
  - Em Linux VM você precisa configurar PulseAudio/ALSA e encaminhar áudio do microfone (por exemplo usando RDP com redirecionamento, USB over IP ou WebRTC/portal) e garantir que a VM possa acessar o dispositivo de entrada. Também é necessário X11/Wayland se quiser interface gráfica, e permissões para enviar eventos de teclado/ratão (uinput).
  - Se o objetivo é apenas treinar/rodar modelos de ASR (sem interface Talon), Azure (GPU) ou Colab funciona bem.

Se quiser, eu preparo:
- Um guia passo-a-passo para instalar o Talon Voice (community) em uma Azure VM Windows (com RDP + redirecionamento de áudio) — ou
- Um script / ARM template + script de provisionamento para criar a VM e instalar dependências (especifique Windows ou Ubuntu), ou
- Um notebook Colab com exemplos de rodar modelos de transcrição (se seu foco for ASR só).

Diga qual Talon e qual opção prefere (Azure Windows / Azure Linux / Colab), e eu monto o plano detalhado e os comandos/scripts.

## @felipecalado45

Qual alternativa para usar taylon no vs code para rodar com mãos livres no sistema operacional windows 10 em um computador com pouca ram

## Copilot

Primeiro: você quis dizer “Talon” (Talon Voice) ou outro “taylon”? E quer controle por voz totalmente offline ou aceita usar um serviço na nuvem (melhor reconhecimento, mas precisa de internet)? Também me diga quanta RAM tem a máquina (ex.: 4 GB, 8 GB) — isso influencia a recomendação.

Enquanto responde, aqui estão alternativas práticas e leves para ter “mãos livres” no VS Code no Windows 10 numa máquina com pouca RAM, com prós/cons e um setup recomendado.

Resumo rápido das alternativas
- Opção A — Mais leve / sem instalar modelos: Windows Speech Recognition (WSR) + WSR Macros ou AutoHotkey
  - Prós: quase zero de RAM extra, já vem no Windows; simples.
  - Contras: precisão e vocabulário limitados; configuração de macros necessária.
  - Recomendada se você precisa de solução imediata e offline com pouca RAM.

- Opção B — Melhor precisão (requer internet): cliente leve que usa uma API de STT (Google/Azure/OpenAI) + script local para enviar teclas ao VS Code
  - Prós: muito mais preciso; fácil mapear comandos complexos.
  - Contras: precisa de internet; depende de conta/API; consome banda (mas pouca RAM local).

- Opção C — ASR local (offline) com modelos pequenos: whisper.cpp / Vosk (modelos tiny/base)
  - Prós: offline; boas opções de modelos pequenos que rodam em CPU.
  - Contras: mesmo modelos “tiny” podem usar CPU e memória; precisa compilar/instalar.

Recomendação prática para baixa RAM (passo-a-passo breve)
Sugiro começar pela Opção A (WSR + AutoHotkey). É a mais leve e costuma ser suficiente para controlar VS Code (abrir paleta, navegar, salvar, executar atalhos). Se depois quiser mais acurácia, passar para a Opção B ou C.

Opção A — WSR + AutoHotkey (setup mínimo)
1) Ativar Windows Speech Recognition
   - Painel de Controle → Facilidade de Acesso → Reconhecimento de Fala → Configurar microfone / iniciar reconhecimento de fala.
2) Instalar Windows Speech Recognition Macros (WSR Macros) ou usar o próprio recurso de comando do WSR para ligar frases a atalhos. (WSR Macros é uma ferramenta da Microsoft que permite mapear frases a ações; embora legada, funciona no Win10.)
3) Instalar AutoHotkey (leve) para executar ações/atalhos no VS Code quando um macro dispara.
4) Criar scripts AutoHotkey para realizar tarefas comuns no VS Code (ex.: abrir paleta, salvar, rodar terminal, mover cursor, selecionar linhas).

Exemplo simples de AutoHotkey (script.ahk)
; script.ahk — mapeia nomes de janelas para atalho
#IfWinActive ahk_exe Code.exe
F1::Send ^+p        ; F1 abre "Command Palette" no VS Code (Ctrl+Shift+P)
F2::Send ^s         ; F2 salva (Ctrl+S)
F3::Send ^`         ; F3 abre terminal (Ctrl+`)
#IfWinActive

- No WSR Macros, configure a frase “Paleta de Comando” para enviar a tecla F1 (ou executar o script.ahk). Dessa forma você não precisa de muito software: WSR escuta e aciona um atalho que o AHK trata dentro do VS Code.

Opção B — Cliente leve + API de STT + pyautogui/keyboard (mais preciso, precisa internet)
- Instalar Python (3.x), pip install SpeechRecognition keyboard pyautogui
- Usar a recognizer Google (testes) ou a API de sua escolha (recomendo teste com Google/Azure/OpenAI).
Exemplo mínimo (teste; exige pyaudio ou sounddevice):
import speech_recognition as sr
import keyboard

r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='pt-BR')
            print(text)
            if "paleta" in text:
                keyboard.send('ctrl+shift+p')
            elif "salvar" in text:
                keyboard.send('ctrl+s')
        except Exception as e:
            print("Erro:", e)

- Vantagem: você controla exatamente quais frases disparam quais ações. Desvantagem: pyaudio e dependências podem ser chato no Windows, mas ainda é razoavelmente leve.

Opção C — whisper.cpp / Vosk (offline)
- Se você não quer internet e tem ao menos 4–8 GB RAM, use whisper.cpp (com modelos tiny/base) ou Vosk com modelos pequenos. whisper.cpp tem binários otimizados para CPU que usam pouca memória.
- Fluxo: rodar processo do whisper.cpp que escreve texto reconhecido em stdout, e um script (Python, AutoHotkey) lê esse texto e dispara atalhos.

Considerações práticas e limites
- Controle completo de “mouse em nível do sistema” ou macros muito avançadas (gestos, janelas fora do foco) pode exigir permissões e ferramentas extras (uinput, drivers), mas para controlar VS Code usando atalhos, as abordagens acima bastam.
- Se RAM < 4 GB: evite rodar modelos locais grandes. Use WSR ou serviços na nuvem.
- Se você precisa de comando por voz altamente programático (expressões, edição de código com seleções complexas), Talon é ideal — mas Talon exige recursos e configuração; daí escolher cloud + AHK ou WSR é um tradeoff prático.

Quer que eu:
- Envie um passo-a-passo detalhado para a Opção A (WSR + WSR Macros + AutoHotkey) com instruções e exemplos de macros e scripts prontos para colar? OU
- Prepare um script Python de exemplo para usar a Opção B (usando Google/WS API) e integração com VS Code?
- Ou prefere que eu explique como tentar whisper.cpp (Opção C) em máquina com X GB de RAM?

## @felipecalado45

Meu computador tem apenas 4 gb de ram então a opção b um cliente leve que usa api de stt mas no script no local é a melhor opção para mim. Tenho conta de estudante no azure e portanto tem api de speech service. Procuro uma solução já pronta para esta demanda. Pretendo apenas instalar alguma aplicação e script ou extensão configurar com ape e configurar o uso no vs code. 

## Copilot

Perfeito — com 4 GB de RAM a melhor escolha é usar o Azure Speech (sua conta já tem) com um cliente local muito leve que faz:
- captura do microfone (usando o Azure Speech SDK),
- envia o texto reconhecido para um script local que dispara atalhos no VS Code (usando pyautogui).

Vou te dar um pacote “pronto para usar”: comandos para instalar, um script Python completo (bastante leve) e instruções para configurar no Windows 10. Esse fluxo é offline/local apenas para integrar com a API do Azure (reconhecimento na nuvem) — pouca RAM usada localmente.

Resumo do que faremos
1. Instalar Python 3.8+ e criar um venv (opcional).
2. Instalar bibliotecas: azure-cognitiveservices-speech + pyautogui.
3. Criar um arquivo config.json com sua chave e região do Azure Speech.
4. Colar e executar o script Python que faz reconhecimento contínuo e mapeia frases para teclas no VS Code.
5. Testar e customizar mapeamentos de voz -> ações.

Requisitos
- Windows 10, microfone configurado (Painel de Controle → Som → Gravação).
- Python 3.8+ instalado (recomendo 3.8 ou 3.10).
- Conta Azure Speech (key + region).
- Fechar apps pesados para economizar RAM.

Instalação (passo a passo)
1) Instale Python (se já tem, pule)
- Baixe do site python.org e marque “Add Python to PATH”.
2) Crie um diretório para o projeto, abra PowerShell ali:
mkdir C:\voice-vscode
cd C:\voice-vscode
python -m venv venv
.\venv\Scripts\Activate.ps1   # PowerShell; no cmd: venv\Scripts\activate.bat
3) Instale dependências:
pip install --upgrade pip
pip install azure-cognitiveservices-speech pyautogui

(Obs.: azure-cognitiveservices-speech usa a captura de áudio do Windows internamente — não precisa instalar pyaudio.)

4) Crie um arquivo config.json no mesmo diretório com sua chave e região:
{
  "AZURE_KEY": "SUA_CHAVE_AQUI",
  "AZURE_REGION": "sua-regiao"  // ex: brazilsouth, westus2, etc.
}

Script Python pronto (cole em voice_control.py)
Salve esse conteúdo em voice_control.py:

import os
import json
import time
import re
import threading
import pyautogui
import azure.cognitiveservices.speech as speechsdk

# Carregar config
cfg_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.exists(cfg_path):
    raise SystemExit("Crie config.json com AZURE_KEY e AZURE_REGION")

with open(cfg_path, "r", encoding="utf-8") as f:
    cfg = json.load(f)

KEY = cfg.get("AZURE_KEY")
REGION = cfg.get("AZURE_REGION")
if not KEY or not REGION:
    raise SystemExit("Coloque AZURE_KEY e AZURE_REGION no config.json")

# Configuração do Azure Speech
speech_config = speechsdk.SpeechConfig(subscription=KEY, region=REGION)
speech_config.speech_recognition_language = "pt-BR"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# Mapeamento: frases -> funções que executam ações (atalhos no VS Code)
def cmd_command_palette():
    pyautogui.hotkey('ctrl', 'shift', 'p')

def cmd_save_file():
    pyautogui.hotkey('ctrl', 's')

def cmd_open_terminal():
    # Ctrl+` para abrir terminal integrado
    pyautogui.hotkey('ctrl', '`')

def cmd_run_debug():
    # Exemplo: iniciar depuração (F5)
    pyautogui.press('f5')

def cmd_close_editor():
    pyautogui.hotkey('ctrl', 'w')

# Dicionário simples (frase lower -> função)
COMMANDS = {
    r"\bpaleta( de comando)?\b": cmd_command_palette,
    r"\bsalvar( arquivo| arquivo atual)?\b": cmd_save_file,
    r"\babrir terminal\b": cmd_open_terminal,
    r"\brodar( sem depuração| sem depurar)?\b": lambda: pyautogui.hotkey('ctrl','f5'),
    r"\brodar\b": cmd_run_debug,
    r"\bfechar editor\b": cmd_close_editor,
}

# Processar reconhecimento
def handle_recognized(evt):
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        text = evt.result.text.strip().lower()
        print("Reconhecido:", text)
        # Checar cada padrão
        for pattern, func in COMMANDS.items():
            if re.search(pattern, text):
                print(f"Comando detectado ({pattern}) -> executando.")
                try:
                    # Coloque foco no VS Code antes, se quiser:
                    # pyautogui.getWindowsWithTitle("Visual Studio Code")[0].activate()
                    func()
                except Exception as e:
                    print("Erro ao executar ação:", e)
                break
    elif evt.result.reason == speechsdk.ResultReason.NoMatch:
        print("Nenhuma fala reconhecida.")

def session_started(evt):
    print("Sessão de reconhecimento iniciada.")

def session_stopped(evt):
    print("Sessão de reconhecimento parada.")
    # Stop loop principal se quiser:
    # stop_recognition()

def canceled(evt):
    print("Recognize canceled:", evt)

# Conectar callbacks
recognizer.recognized.connect(handle_recognized)
recognizer.session_started.connect(session_started)
recognizer.session_stopped.connect(session_stopped)
recognizer.canceled.connect(canceled)

def main():
    print("Iniciando reconhecimento contínuo (diga os comandos configurados).")
    recognizer.start_continuous_recognition()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Parando reconhecimento.")
    finally:
        recognizer.stop_continuous_recognition()

if __name__ == "__main__":
    main()

Como usar
1) Abra VS Code (ou coloque o VS Code em foco). O script enviará teclas para a janela ativa — recomenda-se deixar a janela do VS Code ativa enquanto usa comandos.
2) Execute no PowerShell (com venv ativado):
python voice_control.py
3) Fale as frases (em pt-BR) mapeadas — por exemplo: “paleta de comando”, “salvar”, “abrir terminal”, “rodar”, “fechar editor”.

Personalização
- Para adicionar comandos, edite o dicionário COMMANDS. A chave é uma regex que casa com o texto reconhecido; o valor é uma função Python que executa pyautogui.hotkey ou pyautogui.press.
- Pode ativar um atalho para abrir paleta e então digitar um comando: pyautogui.hotkey('ctrl','shift','p'); time.sleep(0.3); pyautogui.typewrite('>git: clone'); pyautogui.press('enter')
- Se quiser mais robustez, ative uma função que primeiro ativa a janela do VS Code:
win = pyautogui.getWindowsWithTitle("Visual Studio Code")
if win: win[0].activate()

Dicas para rodar com 4 GB RAM
- Feche Chrome/Edge/Outros processos grandes enquanto usar o reconhecimento.
- Não rode VS Code com muitas extensões pesadas ao mesmo tempo.
- O cliente Python + Azure usa pouca RAM; o processamento STT ocorre no Azure.
- Se quiser rodar sem terminal visível: crie um atalho que execute pythonw.exe voice_control.py (pythonw oculta a janela do console).

Permissões e problemas comuns
- Microfone: verifique Configurações → Privacidade → Microfone → permitir apps. Teste o microfone no Gravador de Voz.
- Se o Azure der erro de autenticação, verifique chave e região no config.json.
- Latência: há pequena latência (depende da rede). Se quiser respostas mais rápidas e toleráveis para comandos curtos, o Azure normalmente é responsivo (<500ms-1s).
- Se a detecção errar frequentemente, ajuste linguagem (speech_config.speech_recognition_language = "pt-BR") e fale frases curtas e claras.

Iniciar com um atalho no Windows
- Crie atalho para pythonw.exe C:\voice-vscode\voice_control.py
- Coloque esse atalho em %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup para iniciar com o Windows.

Exemplo de comandos úteis para VS Code (sugestão de mapeamento)
- “paleta de comando” -> Ctrl+Shift+P
- “salvar” -> Ctrl+S
- “abrir terminal” -> Ctrl+`
- “fechar arquivo” -> Ctrl+W
- “ir para linha [número]” (poderia ser implementado lendo número no texto e fazendo Ctrl+G + digitar número) — posso te ajudar a implementar esse caso se quiser.

Quer que eu:
- Gere um package zip com o script e config.json de exemplo? (te envio o conteúdo e instruções)
- Adicione exemplos de comandos mais avançados (ex.: edição de código, selecionar palavra, duplicar linha)?
- Crie a versão que ativa a janela do VS Code automaticamente antes de enviar atalhos?

Diga qual das opções quer que eu entregue agora (zip, mais comandos, ou script que faz "ir para linha X") e eu adapto o script pronto para você.

## @felipecalado45

Gere um package zip com o script e config.json de exemplo? (me envio o conteúdo e instruções)

## Copilot

Aqui estão todos os arquivos do pacote pronto para você criar e compactar (.zip). Copie cada bloco para um arquivo com o nome indicado dentro de uma pasta (ex.: C:\voice-vscode), substitua a chave/região no config.json e compacte a pasta. Também dou instruções para criar venv, instalar dependências e executar.

Arquivos do pacote
- voice_control.py
- config.json.example
- requirements.txt
- setup.ps1 (script PowerShell para criar venv e instalar)
- start.bat (iniciar com console)
- start_hidden.bat (iniciar sem console, usando pythonw)
- README.txt

=== voice_control.py ===
import os
import json
import time
import re
import pyautogui
import azure.cognitiveservices.speech as speechsdk

# Carregar config
cfg_path = os.path.join(os.path.dirname(__file__), "config.json")
if not os.path.exists(cfg_path):
    raise SystemExit("Crie config.json (use config.json.example como modelo) contendo AZURE_KEY e AZURE_REGION")

with open(cfg_path, "r", encoding="utf-8") as f:
    cfg = json.load(f)

KEY = cfg.get("AZURE_KEY")
REGION = cfg.get("AZURE_REGION")
if not KEY or not REGION:
    raise SystemExit("Coloque AZURE_KEY e AZURE_REGION no config.json")

# Configuração do Azure Speech
speech_config = speechsdk.SpeechConfig(subscription=KEY, region=REGION)
speech_config.speech_recognition_language = cfg.get("LANG", "pt-BR")
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# Funções que executam ações (atalhos no VS Code)
def focus_vscode():
    try:
        wins = pyautogui.getWindowsWithTitle("Visual Studio Code")
        if wins:
            wins[0].activate()
            time.sleep(0.15)
    except Exception:
        # getWindowsWithTitle pode não funcionar em todas as instalações; ignorar falha
        pass

def cmd_command_palette():
    focus_vscode()
    pyautogui.hotkey('ctrl', 'shift', 'p')

def cmd_save_file():
    focus_vscode()
    pyautogui.hotkey('ctrl', 's')

def cmd_open_terminal():
    focus_vscode()
    pyautogui.hotkey('ctrl', '`')

def cmd_run_debug():
    focus_vscode()
    pyautogui.press('f5')

def cmd_close_editor():
    focus_vscode()
    pyautogui.hotkey('ctrl', 'w')

def cmd_go_to_line(match):
    # Exemplo: "ir para linha 42"
    num = match.group(1)
    try:
        n = int(num)
    except:
        return
    focus_vscode()
    pyautogui.hotkey('ctrl', 'g')
    time.sleep(0.15)
    pyautogui.typewrite(str(n))
    pyautogui.press('enter')

# Mapeamento: regex -> função (se função precisa da match, ela recebe o match)
COMMANDS = [
    (r"\bpaleta( de comando)?\b", lambda m: cmd_command_palette()),
    (r"\bsalvar( arquivo| arquivo atual)?\b", lambda m: cmd_save_file()),
    (r"\babrir terminal\b", lambda m: cmd_open_terminal()),
    (r"\brodar( sem depuração| sem depurar)?\b", lambda m: pyautogui.hotkey('ctrl','f5')),
    (r"\brodar\b", lambda m: cmd_run_debug()),
    (r"\bfechar( arquivo| editor)?\b", lambda m: cmd_close_editor()),
    (r"\bir para linha\s+(\d+)\b", lambda m: cmd_go_to_line(m)),
]

def handle_recognized(evt):
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        text = evt.result.text.strip().lower()
        print("Reconhecido:", text)
        for pattern, func in COMMANDS:
            m = re.search(pattern, text)
            if m:
                print(f"Comando detectado ({pattern}) -> executando.")
                try:
                    func(m)
                except Exception as e:
                    print("Erro ao executar ação:", e)
                break
    elif evt.result.reason == speechsdk.ResultReason.NoMatch:
        print("Nenhuma fala reconhecida.")

def session_started(evt):
    print("Sessão de reconhecimento iniciada.")

def session_stopped(evt):
    print("Sessão de reconhecimento parada.")

def canceled(evt):
    print("Reconhecimento cancelado:", evt)

recognizer.recognized.connect(handle_recognized)
recognizer.session_started.connect(session_started)
recognizer.session_stopped.connect(session_stopped)
recognizer.canceled.connect(canceled)

def main():
    print("Iniciando reconhecimento contínuo. Fale um dos comandos configurados.")
    recognizer.start_continuous_recognition()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Parando reconhecimento.")
    finally:
        recognizer.stop_continuous_recognition()

if __name__ == "__main__":
    main()

=== config.json.example ===
{
  "AZURE_KEY": "COLE_SUA_CHAVE_AQUI",
  "AZURE_REGION": "sua-regiao-aqui",
  "LANG": "pt-BR"
}
(Substitua AZURE_KEY e AZURE_REGION e renomeie para config.json antes de rodar.)

=== requirements.txt ===
azure-cognitiveservices-speech
pyautogui

(Se quiser ativar foco automático de janela em algumas instalações, instale também pygetwindow; mas pyautogui normalmente instala dependências necessárias.)

=== setup.ps1 ===
# Execute este script no PowerShell (ideia: abra PowerShell como administrador se necessário)
$project = "$PSScriptRoot"
python -V 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python não encontrado no PATH. Instale o Python 3.8+ e marque 'Add to PATH'."
    exit 1
}
python -m venv venv
& "$project\venv\Scripts\Activate.ps1"
pip install --upgrade pip
pip install -r "$project\requirements.txt"
Write-Host "Ambiente criado e dependências instaladas. Ative com: .\venv\Scripts\Activate.ps1"

=== start.bat ===
@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
python voice_control.py
pause

=== start_hidden.bat ===
@echo off
cd /d "%~dp0"
REM Usa pythonw para rodar sem console. Certifique-se de ter venv ativado no ambiente ou caminho absoluto do pythonw.
call venv\Scripts\activate.bat
pythonw "%~dp0voice_control.py"

=== README.txt ===
Voice control para VS Code usando Azure Speech
==============================================

1) Preparação
- Crie uma pasta, copie os arquivos do pacote para dentro.
- Renomeie config.json.example para config.json e coloque sua AZURE_KEY e AZURE_REGION.
- Abra PowerShell na pasta e execute:
  .\setup.ps1
  (ou manualmente: python -m venv venv ; .\venv\Scripts\Activate.ps1 ; pip install -r requirements.txt)

2) Execução
- Abra Visual Studio Code (deixe a janela ativa enquanto usa).
- No PowerShell execute:
  .\start.bat
  ou use start_hidden.bat para rodar sem console.

3) Comandos padrões incluídos
- "paleta de comando" -> abre Command Palette (Ctrl+Shift+P)
- "salvar" -> Ctrl+S
- "abrir terminal" -> Ctrl+`
- "rodar" -> F5
- "rodar sem depuração" -> Ctrl+F5
- "fechar arquivo" -> Ctrl+W
- "ir para linha X" -> abre ir-para-linha e vai para o número

4) Customização
- Edite voice_control.py: adicione novos padrões em COMMANDS (regex) e funções que chamem pyautogui.hotkey/typewrite/press.
- Para digitar texto após abrir a paleta, use time.sleep(0.15) entre ações.

5) Observações importantes
- Substitua config.json com sua chave privada — não faça commit desse arquivo em repositórios públicos.
- Feche apps pesados (Chrome) para poupar RAM.
- Verifique Configurações -> Privacidade -> Microfone para permitir apps usarem o microfone.
- Latência depende da conexão de rede para Azure Speech.

Como compactar e criar o .zip
- Método 1 (Windows Explorer):
  1. Selecione a pasta (ex.: C:\voice-vscode).
  2. Clique direito → Enviar para → Pasta compactada (zipada).
- Método 2 (PowerShell):
  Compress-Archive -Path "C:\caminho\para\voice-vscode\*" -DestinationPath "C:\caminho\para\voice-vscode.zip"

Segurança
- Não compartilhe config.json com a chave em locais públicos. Use config.json.example no repositório e mantenha config.json local.

Extras que posso gerar (me diga qual quer que eu inclua antes de você criar o zip):
- Script para "ir para função X" ou macros mais avançadas (selecionar, duplicar linha).
- Versão do voice_control.py com suporte a um modo de confirmação (por exemplo: fala "salvar" -> confirma com "sim" antes de executar).
- Arquivo .exe gerado (não posso compilar aqui, mas posso fornecer instruções para criar com pyinstaller).

Próximo passo
Se quiser, eu monto um pacote .zip pronto aqui no chat com instruções para baixar — ou, se preferir, eu te envio somente um arquivo .zip via link (não posso hospedar, então preciso que você me diga como prefere receber: instruções passo a passo para criar localmente ou gerar um comando PowerShell/ZIP que você cole e execute). O que prefere?
