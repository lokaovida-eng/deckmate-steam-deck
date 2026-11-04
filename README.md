# DeckMate

**A system-support assistant focused on Steam Deck and Linux.**

[![Download DeckMate for Linux](https://img.shields.io/badge/DOWNLOAD-DeckMate%20for%20Linux-167a45?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/lokaovida-eng/deckmate-steam-deck/archive/refs/heads/main.zip)
[![How to install and start](https://img.shields.io/badge/How%20to%20install-and%20start-3776AB?style=for-the-badge)](#quick-start-steam-deck)

**New here?** Download the ZIP, extract it, and follow the short setup below.
This download contains the Python source code, not a one-click installer.
An experimental AppImage build workflow exists, but no AppImage has been
published yet. The app also needs the official GitHub Copilot CLI for sign-in;
that CLI is not included in the AppImage.

DeckMate is an early-stage desktop application built with Python and Qt Widgets
(PySide6). It connects to the official GitHub Copilot SDK to answer questions,
inspect available system information, and guide troubleshooting. It is not
affiliated with Valve, KDE, or GitHub.

The window uses a translucent black background while chat panels, text, buttons,
and dialogs stay opaque. KDE Plasma on X11/XWayland additionally receives a
best-effort KWin blur request. Blur depends on compositor support and settings;
other desktops keep the translucent background without relying on KWin-specific
effects. The app does not set a global window-opacity value.

## Project status

DeckMate is an experimental prototype distributed as source code. It is **not
available in KDE Discover or Flathub**. Flathub maintainers reviewed a
pre-submission question and said the project is not currently eligible because
its development history is too short. No Flatpak package has been prepared;
host access, sandbox restrictions, external Copilot runtime distribution, and
other requirements still need review. The current Flathub policy also prohibits
AI-generated or AI-assisted manifests, and its inclusion rules assess whether
host system utilities and apps needing broad host access are suitable. These
design and policy questions must be resolved before packaging or submission;
there is no reliable acceptance timeline.

The project primarily targets Steam Deck and Linux. Other operating systems and
hardware have not been validated. Diagnostics depend on the host, installed
tools, account access, network connectivity, and SDK permissions. DeckMate
cannot guarantee that it can diagnose or repair every issue.

## Quick start (Steam Deck)

1. Select **DOWNLOAD — DeckMate for Linux** at the top of this page and save
   the ZIP file.
2. In Desktop Mode, open **Downloads** in Dolphin and extract the ZIP.
3. Install the official GitHub Copilot CLI in Konsole by following its
   [Linux installation instructions](https://github.com/github/copilot-cli#installation).
   The DeckMate SDK runtime and the Copilot CLI are separate downloads.
4. Open Konsole in the extracted `deckmate-steam-deck-main` folder and run:

   ```bash
   copilot login
   python3 -m venv .venv
   .venv/bin/python -m pip install --upgrade pip
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python -m copilot download-runtime
   .venv/bin/python assistente.py
   ```

5. In DeckMate, select **Connect** if you need to sign in again. A GitHub
   account with Copilot access and an internet connection are required.

The commands above prepare and start the app; they do not create a desktop
shortcut. If setup reports that `python3 -m venv` is unavailable, or Copilot
cannot connect, see [all setup details and troubleshooting](#run-from-source).
DeckMate is source code today, not a one-click installer, and it is not listed
in KDE Discover or Flathub.

Prefer downloading just the application file? Get [`assistente.py`](https://github.com/lokaovida-eng/deckmate-steam-deck/raw/main/assistente.py).

The Flathub pre-submission inquiry was declined because the repository then had
only two commits, published 14 hours earlier. The maintainer explicitly cited
insufficient development history as the reason; this was not a review of a
Flatpak package. There is no guaranteed commit-count or age threshold. See
[the maintainer's response](https://github.com/flathub/flathub/issues/10867#issuecomment-6468628491)
and [CONTRIBUTING.md](CONTRIBUTING.md) for the project's release-readiness
checks. Real-world use and ongoing maintenance still need to be demonstrated.

## Feedback and testing

DeckMate is experimental. Reports from actual Linux desktops help us find
environment-specific problems that automated tests cannot reproduce. When
reporting an issue, include the app version or commit, distribution and desktop
session, and steps to reproduce. Never attach credentials, tokens, private
Copilot conversations, or unredacted personal logs.

## Development disclosure

Some source code and documentation in this prototype were created or revised
with generative-AI assistance. The maintainer remains responsible for reviewing
and testing changes. Before preparing a Flathub submission, follow its
[current generative-AI policy](https://docs.flathub.org/docs/for-app-authors/requirements#generative-ai-policy);
in particular, Flathub manifests must not be generated or assisted by AI.

## Requirements

- Python 3.10 or newer
- PySide6 and a graphical desktop with Qt support
- The official GitHub Copilot CLI for sign-in (not bundled with the AppImage)
- A GitHub account with access to GitHub Copilot
- Network access to the Copilot service
- The SDK downloads its separate Copilot runtime when needed

## Run from source

On Steam Deck, switch to Desktop Mode and open Konsole. On other Linux
distributions, use their normal graphical desktop and package-management tools.

```bash
curl -fsSL https://gh.io/copilot-install | bash
copilot login
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m copilot download-runtime
.venv/bin/python assistente.py
```

The first command installs GitHub's official Copilot CLI for your user account;
it is separate from the SDK runtime downloaded by the next command. If the
`copilot` command is not found immediately after installation, reopen Konsole.
The **Connect** button launches `copilot login` in a supported terminal. A
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

---

## Português (Brasil)

O DeckMate é um protótipo experimental de assistente para Steam Deck e Linux.
Ele usa Python, Qt Widgets (PySide6) e o SDK oficial do GitHub Copilot. Não é
afiliado à Valve, KDE ou GitHub.

[![BAIXAR DeckMate para Linux](https://img.shields.io/badge/BAIXAR-DeckMate%20para%20Linux-167a45?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/lokaovida-eng/deckmate-steam-deck/archive/refs/heads/main.zip)
[![Como instalar e abrir](https://img.shields.io/badge/Como%20instalar-e%20abrir-3776AB?style=for-the-badge)](#in%C3%ADcio-r%C3%A1pido-steam-deck)

Existe um fluxo experimental para gerar um AppImage, mas ainda não há um
AppImage publicado. O programa também precisa do CLI oficial do GitHub Copilot
para fazer login; esse CLI não vem incluído no AppImage.

O fundo preto da janela é translúcido, enquanto os painéis de conversa, textos,
botões e diálogos permanecem opacos. No KDE Plasma com X11/XWayland, o app
também solicita o desfoque de fundo ao KWin, quando disponível. O desfoque
depende do suporte e das configurações do compositor; em outros desktops, o
fundo translúcido não depende de efeitos específicos do KWin. O app não aplica
opacidade global à janela.

### Início rápido (Steam Deck)

1. Clique em **BAIXAR — DeckMate para Linux** no início desta página e salve o
   arquivo ZIP.
2. No Modo Desktop, abra **Downloads** no Dolphin e extraia o ZIP.
3. Instale o CLI oficial do GitHub Copilot no Konsole seguindo as
   [instruções para Linux](https://github.com/github/copilot-cli#installation).
   O runtime do SDK DeckMate e o CLI do Copilot são downloads separados.
4. Abra o Konsole dentro da pasta extraída `deckmate-steam-deck-main` e execute:

   ```bash
   copilot login
   python3 -m venv .venv
   .venv/bin/python -m pip install --upgrade pip
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python -m copilot download-runtime
   .venv/bin/python assistente.py
   ```

5. No DeckMate, selecione **Connect** se precisar entrar novamente. É necessária
   uma conta GitHub com acesso ao Copilot e conexão com a internet.

Esses passos preparam e abrem o programa; eles não criam um atalho na área de
trabalho. Se `python3 -m venv` não estiver disponível ou o Copilot não conectar,
veja [as instruções completas e solução de problemas](#executar-a-partir-do-c%C3%B3digo).
Hoje o DeckMate é código-fonte, não um instalador de um clique, e ainda não está
no KDE Discover ou no Flathub.

Quer baixar somente o arquivo do aplicativo? Baixe [`assistente.py`](https://github.com/lokaovida-eng/deckmate-steam-deck/raw/main/assistente.py).

**O aplicativo ainda não está no KDE Discover nem no Flathub.** Os mantenedores
do Flathub recusaram a consulta de pré-submissão porque, naquele momento, o
repositório tinha apenas dois commits publicados havia 14 horas. Essa foi a
razão explicitamente citada; não houve avaliação de um pacote Flatpak. Não
existe um número mínimo garantido de commits ou dias. O histórico contínuo,
uso real e manutenção ainda precisam ser demonstrados. Veja a
[resposta do mantenedor](https://github.com/flathub/flathub/issues/10867#issuecomment-6468628491)
e os critérios de release em [CONTRIBUTING.md](CONTRIBUTING.md). Também será
necessário resolver o acesso do aplicativo ao sistema dentro do sandbox, como
distribuir o runtime externo do Copilot, e confirmar se o tipo de utilitário e
as permissões atendem às regras atuais do Flathub. Os manifestos do Flathub não
podem ser escritos ou assistidos por IA. Essas questões precisam ser resolvidas
antes de empacotar ou enviar o aplicativo; não há prazo garantido de aprovação.

### Feedback e testes

O DeckMate ainda é experimental. Relatos de uso em desktops Linux reais ajudam
a encontrar problemas que testes automatizados não reproduzem. Ao relatar um
problema, informe a versão ou commit do app, a distribuição, a sessão gráfica e
os passos para reproduzi-lo. Nunca anexe credenciais, tokens, conversas
privadas do Copilot ou logs pessoais sem remover dados sensíveis.

### Transparência de desenvolvimento

Partes do código-fonte e da documentação deste protótipo foram criadas ou
revisadas com auxílio de inteligência artificial generativa. O mantenedor
continua responsável por revisar e testar as mudanças. Antes de preparar uma
submissão ao Flathub, siga a
[política atual de IA generativa](https://docs.flathub.org/docs/for-app-authors/requirements#generative-ai-policy);
em particular, manifestos do Flathub não podem ser criados ou assistidos por IA.

### Requisitos

- Python 3.10 ou mais recente, PySide6 e um desktop gráfico com suporte a Qt
- CLI oficial do GitHub Copilot para login (não incluído no AppImage)
- Conta com acesso ao GitHub Copilot
- Acesso à internet; o SDK baixa seu runtime separado quando necessário

### Executar a partir do código

No Steam Deck, entre no Modo Desktop e abra o Konsole:

```bash
curl -fsSL https://gh.io/copilot-install | bash
copilot login
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m copilot download-runtime
.venv/bin/python assistente.py
```

O primeiro comando instala o CLI oficial do GitHub Copilot para sua conta; ele
é separado do runtime do SDK baixado pelo próximo comando. Se `copilot` não for
reconhecido logo após a instalação, feche e reabra o Konsole. O botão
**Connect** abre `copilot login` em um terminal compatível. É necessária uma
conta com acesso ao GitHub Copilot.

### Privacidade e segurança

As perguntas e informações usadas nas respostas são enviadas ao GitHub Copilot.
Não compartilhe senhas, tokens, chaves privadas ou logs sensíveis. Ações no
sistema podem alterar o aparelho: leia o pedido de autorização e aprove apenas
o que compreender. A janela de permissão não garante que uma ação seja segura.
Este protótipo ainda não passou por uma auditoria de segurança independente.
