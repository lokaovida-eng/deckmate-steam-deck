# DeckMate

**A system-support assistant focused on Steam Deck and Linux.**

DeckMate is an early-stage desktop application built with Python and
CustomTkinter. It connects to the official GitHub Copilot SDK to answer
questions, inspect available system information, and guide troubleshooting.
It is not affiliated with Valve, KDE, or GitHub. On KDE Plasma under
X11/XWayland, the app requests a translucent window with KWin background blur.
Blur depends on compositor support and settings; other display backends keep
the supported opacity effect without claiming blur.

## Project status

DeckMate is an experimental prototype distributed as source code. It is **not
available in KDE Discover or Flathub**. Flathub maintainers reviewed a
pre-submission question and said the project is not currently eligible because
its development history is too short. No Flatpak package has been prepared;
host access, sandbox restrictions, and other requirements still need review.

The project primarily targets Steam Deck and Linux. Other operating systems and
hardware have not been validated. Diagnostics depend on the host, installed
tools, account access, network connectivity, and SDK permissions. DeckMate
cannot guarantee that it can diagnose or repair every issue.

## Requirements

- Python 3.10 or newer
- A graphical desktop with Tcl/Tk support
- A GitHub account with access to GitHub Copilot
- Network access to the Copilot service
- The GitHub Copilot CLI/runtime required by the SDK

## Run from source

On Steam Deck, switch to Desktop Mode and open Konsole. On other Linux
distributions, use their normal graphical desktop and package-management tools.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m copilot download-runtime
copilot login
.venv/bin/python assistente.py
```

The `copilot login` command must be available from your installation of the
official GitHub Copilot CLI. If it is not installed or cannot be found, use the
app's **Connect** button and follow the displayed sign-in instructions. A
Copilot subscription/account with access is required.

## Safety and privacy

Prompts and information used to answer them are sent to GitHub Copilot. Avoid
sharing passwords, tokens, private keys, or sensitive logs. System actions can
change the device. Inspect each requested action and approve only actions you
understand; the permission dialog does not make an action safe by itself.

DeckMate aims to prefer read-only checks, distinguish SteamOS from general
Linux, and protect user data. This prototype has not undergone independent
security review.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for the current development and testing
process. Flathub guidance and known limitations are tracked in
[issue #10867](https://github.com/flathub/flathub/issues/10867).

## License and credits

DeckMate is distributed under the GNU General Public License, version 3 or later.
See [LICENSE](LICENSE).

Created by **Flavinho PQD 85207**.  
Instagram: <https://www.instagram.com/eagle_85207/>

---

## Português (Brasil)

O DeckMate é um protótipo experimental de assistente para Steam Deck e Linux.
Ele usa Python, CustomTkinter e o SDK oficial do GitHub Copilot. Não é afiliado
à Valve, KDE ou GitHub.
No KDE Plasma com X11/XWayland, o app solicita translucidez e desfoque de fundo
ao KWin. O desfoque depende do suporte e das configurações do compositor; em
outros sistemas gráficos, fica disponível apenas o efeito de opacidade suportado.

**O aplicativo ainda não está no KDE Discover nem no Flathub.** Os mantenedores
do Flathub informaram que o projeto ainda não pode ser enviado porque tem pouco
histórico de desenvolvimento. Ainda não existe pacote Flatpak, e os limites de
acesso ao sistema precisam ser avaliados.

### Requisitos

- Python 3.10 ou mais recente e suporte a Tcl/Tk
- Conta com acesso ao GitHub Copilot
- Acesso à internet e ao runtime/CLI necessário pelo SDK

### Executar a partir do código

No Steam Deck, entre no Modo Desktop e abra o Konsole:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m copilot download-runtime
copilot login
.venv/bin/python assistente.py
```

O comando `copilot login` requer o CLI oficial do GitHub Copilot instalado e
disponível no terminal. Se não estiver disponível, use o botão **Connect** do
aplicativo e siga as instruções de login. É necessária uma conta com acesso ao
GitHub Copilot.

### Privacidade e segurança

As perguntas e informações usadas nas respostas são enviadas ao GitHub Copilot.
Não compartilhe senhas, tokens, chaves privadas ou logs sensíveis. Ações no
sistema podem alterar o aparelho: leia o pedido de autorização e aprove apenas
o que compreender. A janela de permissão não garante que uma ação seja segura.
Este protótipo ainda não passou por uma auditoria de segurança independente.
