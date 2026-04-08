# Signal MCP Client – Komplett oppsettguide
## WSL2 + Podman + Claude Code på Windows

---

## Arkitektur

```
Windows 11
│
├── WSL2 (Ubuntu 24.04)
│     ├── Podman
│     │     └── signal-cli-rest-api  (container, port 8080)
│     ├── uv + Python
│     │     └── signal-mcp-client    (lytter på Signal)
│     ├── Claude Code                (redigerer filer, git push)
│     ├── Git
│     └── ~/projects/
│           ├── sommerferie2026/     → GitHub Pages
│           └── signal-mcp-client/
│
└── (Docker Desktop ikke nødvendig)
```

---

## Forutsetninger

- Windows 10 (21H2+) eller Windows 11
- eSIM eller Lycamobile SIM-kort med norsk nummer klart
- Anthropic API-nøkkel
- GitHub-konto med repo `arnego/sommerferie2026`

---

## DEL 1 – WSL2-oppsett

### Steg 1.1: Installer WSL2 med Ubuntu

Åpne PowerShell som administrator:

```powershell
wsl --install -d Ubuntu-24.04
```

Start om PCen når installasjonen er ferdig, og fullfør Ubuntu-oppsett (velg brukernavn og passord).

### Steg 1.2: Aktiver systemd i WSL

Dette er nødvendig for Podman og autostart-tjenester.

I Ubuntu-terminalen:

```bash
sudo nano /etc/wsl.conf
```

Legg til:

```ini
[boot]
systemd=true

[automount]
enabled=true
options="metadata"
```

Lagre (Ctrl+X, Y, Enter), deretter restart WSL fra PowerShell:

```powershell
wsl --shutdown
wsl
```

Verifiser at systemd kjører:

```bash
systemctl --version
```

### Steg 1.3: Oppdater Ubuntu og installer grunnpakker

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget nano build-essential
```

### Steg 1.4: Konfigurer Git i WSL

```bash
git config --global user.name "Arnego"
git config --global user.email "din@epost.no"
git config --global credential.helper store
```

---

## DEL 2 – Podman-oppsett

### Steg 2.1: Installer Podman

```bash
sudo apt install -y podman
```

Verifiser:

```bash
podman --version
```

### Steg 2.2: Konfigurer Podman for rootless bruk

```bash
# Aktiver lingering (holder brukerøkten aktiv)
sudo loginctl enable-linger $USER

# Verifiser at subuid/subgid er satt opp
cat /etc/subuid | grep $USER
cat /etc/subgid | grep $USER
```

Hvis disse er tomme:

```bash
sudo usermod --add-subuids 100000-165535 $USER
sudo usermod --add-subgids 100000-165535 $USER
```

### Steg 2.3: Start signal-cli-rest-api

```bash
# Opprett datakatalog
mkdir -p $HOME/.local/share/signal-api

# Start containeren
podman run \
    --name signal-cli-api \
    --replace \
    -p 8080:8080 \
    -v $HOME/.local/share/signal-api:/home/.local/share/signal-cli \
    -e 'MODE=json-rpc' \
    docker.io/bbernhard/signal-cli-rest-api:latest-dev
```

> La dette vinduet stå åpent – containeren logger her. Åpne et nytt terminalvindu for neste steg.

### Steg 2.4: Koble Signal-konto via QR-kode

I Windows-nettleseren, åpne:

```
http://localhost:8080/v1/qrcodelink?device_name=signal-bot
```

På telefonen:
- Signal → Innstillinger → Tilknyttede enheter → + → Skann QR-koden

Bekreft at tilkoblingen fungerer:

```
http://localhost:8080/v1/about
```

### Steg 2.5: Sett opp Podman systemd-tjeneste for autostart

```bash
# Opprett systemd user service-katalog
mkdir -p $HOME/.config/systemd/user/

# Lag service-fil for signal-cli-rest-api
cat << EOF > $HOME/.config/systemd/user/signal-cli-rest-api.service
[Unit]
Description=Signal CLI REST API
After=network.target

[Service]
Restart=on-failure
RestartSec=10
ExecStartPre=-/usr/bin/podman stop signal-cli-api
ExecStartPre=-/usr/bin/podman rm signal-cli-api
ExecStart=/usr/bin/podman run \
    --name signal-cli-api \
    -p 8080:8080 \
    -v %h/.local/share/signal-api:/home/.local/share/signal-cli \
    -e MODE=json-rpc \
    docker.io/bbernhard/signal-cli-rest-api:latest-dev
ExecStop=/usr/bin/podman stop signal-cli-api

[Install]
WantedBy=default.target
EOF

# Aktiver og start tjenesten
systemctl --user daemon-reload
systemctl --user enable signal-cli-rest-api.service
systemctl --user start signal-cli-rest-api.service

# Sjekk status
systemctl --user status signal-cli-rest-api.service
```

---

## DEL 3 – Python og uv

### Steg 3.1: Installer uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Legg til i `.bashrc` for permanent tilgang:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> $HOME/.bashrc
source $HOME/.bashrc
```

Verifiser:

```bash
uv --version
```

> **Merk:** Installer-skriptet printer alltid på slutten hvilken PATH-linje som gjelder – bruk den hvis noe avviker.

---

## DEL 4 – Klargjør repoet i WSL

### Steg 4.1: Verifiser at repoet er på plass

```bash
cd ~/projects/sommerferie2026
git status
```

### Steg 4.2: Klon signal-mcp-client

```bash
git clone https://github.com/piebro/signal-mcp-client.git ~/projects/signal-mcp-client
cd ~/projects/signal-mcp-client
```

### Steg 4.3: Opprett MCP-server-katalog

```bash
mkdir -p ~/projects/mcp-servers/sommerferie2026
```

Kopier `sommerferie2026_server.py` hit (se Del 6).

---

## DEL 5 – Konfigurer signal-mcp-client

### Steg 5.1: Miljøvariabler

Legg til i `$HOME/.bashrc`:

```bash
cat << 'EOF' >> $HOME/.bashrc

# Signal MCP Bot
export ANTHROPIC_API_KEY="sk-ant-DIN-NØKKEL-HER"
export SIGNAL_PHONE_NUMBER="+47BOT-NUMMER-HER"
export SIGNAL_WS_BASE_URL="ws://localhost:8080"
export SIGNAL_HTTP_BASE_URL="http://localhost:8080"
EOF

source $HOME/.bashrc
```

### Steg 5.2: Opprett config.json

```bash
cat << 'EOF' > ~/projects/signal-mcp-client/config.json
{
    "servers": [
        {
            "name": "sommerferie2026",
            "description": "Oppdaterer reiseplanen på arnego.github.io/sommerferie2026.",
            "command": "python3",
            "args": ["/home/arne/projects/mcp-servers/sommerferie2026/sommerferie2026_server.py"],
            "env": {}
        }
    ],

    "group_configs": [
        {
            "group_name_contains": "Sommerferie",
            "system_prompt": "Du er reiseplanassistent for en campingvognferie i juli 2026 fra Kongsberg gjennom Danmark, Tyskland, Nederland, Schwarzwald til Østerrike/Alpene. Du har verktøy for å oppdatere reiseplanen på GitHub Pages. Svar alltid på norsk. Bruk update_travel_plan-verktøyet direkte uten å be om bekreftelse.",
            "servers": ["sommerferie2026"]
        }
    ],

    "default_system_prompt": "Du er en hjelpsom AI-assistent. Svar alltid på norsk."
}
EOF
```

### Steg 5.3: Opprett sessions-katalog

```bash
mkdir -p ~/projects/signal-mcp-client/sessions
```

---

## DEL 6 – sommerferie2026 MCP-server

Opprett `~/projects/mcp-servers/sommerferie2026/sommerferie2026_server.py`:

```bash
nano ~/projects/mcp-servers/sommerferie2026/sommerferie2026_server.py
```

Lim inn innholdet fra `sommerferie2026_server.py` (se egen fil i denne pakken).

Installer avhengigheter:

```bash
pip3 install mcp anthropic --break-system-packages
```

Eller med uv (anbefalt):

```bash
uv tool install mcp
pip3 install anthropic --break-system-packages
```

---

## DEL 7 – Test manuelt

### Steg 7.1: Start signal-mcp-client for testing

```bash
cd ~/projects/signal-mcp-client

uv run signal_mcp_client/main.py \
    --config config.json \
    --session-save-dir ~/projects/signal-mcp-client/sessions \
    --available-models claude-sonnet-4-6 claude-haiku-4-5 claude-opus-4-6 \
    --default-model-name claude-sonnet-4-6 \
    --default-system-prompt "Du er en hjelpsom assistent. Svar på norsk." \
    --default-llm-chat-message-context-limit 50
```

### Steg 7.2: Send testmelding

Send en Signal-melding til bot-nummeret fra telefonen din.
Boten skal svare innen noen sekunder.

Send deretter en oppdatering:
```
Legg til Lübeck som dagstur fra Hamburg i uke 2
```

Sjekk https://arnego.github.io/sommerferie2026/ etter ~30 sekunder.

---

## DEL 8 – Autostart med systemd

### Steg 8.1: Lag systemd-tjeneste for signal-mcp-client

```bash
cat << EOF > $HOME/.config/systemd/user/signal-mcp-client.service
[Unit]
Description=Signal MCP Client
After=network.target signal-cli-rest-api.service
Wants=signal-cli-rest-api.service

[Service]
Environment="ANTHROPIC_API_KEY=sk-ant-DIN-NØKKEL-HER"
Environment="SIGNAL_PHONE_NUMBER=+47BOT-NUMMER-HER"
Environment="SIGNAL_WS_BASE_URL=ws://localhost:8080"
Environment="SIGNAL_HTTP_BASE_URL=http://localhost:8080"
WorkingDirectory=/home/arne/projects/signal-mcp-client
ExecStart=/home/arne/.local/bin/uv run signal_mcp_client/main.py \
    --config config.json \
    --session-save-dir /home/arne/projects/signal-mcp-client/sessions \
    --available-models claude-sonnet-4-6 claude-haiku-4-5 claude-opus-4-6 \
    --default-model-name claude-sonnet-4-6 \
    --default-system-prompt "Du er en hjelpsom assistent. Svar på norsk." \
    --default-llm-chat-message-context-limit 50
Restart=on-failure
RestartSec=30

[Install]
WantedBy=default.target
EOF

# Aktiver tjenesten
systemctl --user daemon-reload
systemctl --user enable signal-mcp-client.service
systemctl --user start signal-mcp-client.service

# Sjekk status og logger
systemctl --user status signal-mcp-client.service
journalctl --user -u signal-mcp-client.service -f
```

### Steg 8.2: Autostart WSL ved Windows-oppstart

**Alternativ A – Automatisk oppsett (anbefalt)**

Kopier `setup_task_scheduler.ps1` og `start_wsl_bot.ps1` til `C:\Users\DITTBRUKERNAVN`.

Åpne PowerShell som administrator og kjør:

```powershell
Set-ExecutionPolicy Bypass -Scope Process
cd $env:USERPROFILE
.\setup_task_scheduler.ps1
```

Dette oppretter Task Scheduler-oppgaven automatisk. Ferdig.

---

**Alternativ B – Manuelt i Task Scheduler**

1. Kopier `start_wsl_bot.ps1` til `C:\Users\DITTBRUKERNAVN`
2. Åpne **Oppgaveplanlegger** → **Opprett grunnleggende oppgave**
3. Navn: `Start WSL Signal Bot`
4. Utløser: **Ved pålogging**
5. Handling: **Start et program**
  - Program: `powershell.exe`
  - Argumenter: `-ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\DITTBRUKERNAVN\start_wsl_bot.ps1"`
6. Fullfør

---

**Test at oppgaven fungerer:**

```powershell
Start-ScheduledTask -TaskName "Start WSL Signal Bot"
```

Vent 15 sekunder, åpne WSL og sjekk:

```bash
systemctl --user status signal-cli-rest-api signal-mcp-client
```

---

## DEL 9 – Claude Code i WSL

### Steg 9.1: Installer Claude Code

```bash
# Installer Node.js (kreves av Claude Code)
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# Installer Claude Code
npm install -g @anthropic-ai/claude-code
```

### Steg 9.2: Bruk Claude Code på repoet

```bash
cd ~/projects/sommerferie2026
claude
```

Claude Code kan nå redigere `index.html` og pushe til GitHub direkte.

---

## DEL 10 – Registrer Lycamobile-nummer i Signal

Når du har aktivert SIM-kortet og notert +47-nummeret:

### Steg 10.1: Registrer nummeret

```bash
curl -X POST http://localhost:8080/v1/register/+47DITT-NUMMER
```

### Steg 10.2: Motta SMS-kode og verifiser

Sett SIM-kortet i telefon, les av SMS-koden:

```bash
curl -X POST http://localhost:8080/v1/register/+47DITT-NUMMER/verifyCode/KODEN
```

### Steg 10.3: Sett Registration Lock PIN

```bash
curl -X POST http://localhost:8080/v1/accounts/+47DITT-NUMMER/registration-lock \
  -H "Content-Type: application/json" \
  -d '{"pin": "EN-KODE-DU-HUSKER"}'
```

### Steg 10.4: Oppdater miljøvariabler

```bash
# Rediger .bashrc
nano $HOME/.bashrc

# Oppdater denne linjen:
export SIGNAL_PHONE_NUMBER="+47DITT-NUMMER"

# Og i systemd-tjenestene:
nano $HOME/.config/systemd/user/signal-mcp-client.service
# Oppdater Environment="SIGNAL_PHONE_NUMBER=+47DITT-NUMMER"

systemctl --user daemon-reload
systemctl --user restart signal-mcp-client.service
```

---

## DEL 11 – Opprett Signal-gruppechat

Dette gjøres på telefonen **etter** at bot-nummeret er registrert i Del 10.

### Steg 11.1: Legg til bot-nummeret som kontakt

På telefonen:
- Legg til bot-nummeret (+47LYCAMOBILE) som kontakt, f.eks. med navn **"Sommerferie Bot"**

### Steg 11.2: Opprett gruppechat i Signal

1. Åpne Signal → trykk på blyant-ikonet → **Ny gruppe**
2. Legg til **Sommerferie Bot** (bot-nummeret)
3. Legg til øvrige familiemedlemmer som skal ha tilgang
4. **Sett gruppenavn til noe som inneholder ****`Sommerferie2026`**

> Dette er viktig – `group_name_contains` i `config.json` er satt til `"Sommerferie2026"`, så gruppen må ha det ordet i navnet for at boten skal bruke riktig system-prompt og MCP-server. F.eks. `"Sommerferie2026 🚐"` eller bare `"Sommerferie2026"`.

### Steg 11.3: Test gruppechatten

Send en melding i gruppen:
```
Hei! Hva er statusen på reiseplanen?
```

Boten skal svare og bruke `read_travel_plan`-verktøyet automatisk.

Send deretter en oppdatering:
```
Legg til Lübeck som dagstur fra Hamburg i uke 2
```

Boten skal committe og pushe til GitHub uten å be om bekreftelse.

---

## Feilsøking

### signal-cli-rest-api svarer ikke
```bash
# Sjekk at containeren kjører
podman ps

# Se logger
podman logs signal-cli-api

# Restart
systemctl --user restart signal-cli-rest-api.service
```

### signal-mcp-client kobler ikke til
```bash
# Sjekk at REST API er oppe
curl http://localhost:8080/v1/about

# Sjekk logger
journalctl --user -u signal-mcp-client.service -n 50
```

### Git push feiler fra WSL
```bash
# Sjekk at credentials er lagret
cat $HOME/.git-credentials

# Autentiser på nytt
cd ~/projects/sommerferie2026
git push
# Skriv inn GitHub brukernavn og Personal Access Token når du blir spurt
```

### uv ikke funnet i systemd
```bash
# Finn full path
which uv
# Typisk: /home/BRUKER/.local/bin/uv
# Bruk full path i ExecStart i stedet for %h/.local/bin/uv
```

---

## Oversikt over filer og plasseringer

```
~/projects/
├── sommerferie2026/                 ← GitHub Pages repo
│   └── index.html
├── signal-mcp-client/               ← klonet repo
│   ├── config.json                  ← prosjektkonfigurasjon
│   └── sessions/                    ← samtalehistorikk
└── mcp-servers/
    └── sommerferie2026/
        └── sommerferie2026_server.py

$HOME/
├── .bashrc                          ← miljøvariabler
├── .config/systemd/user/
│   ├── signal-cli-rest-api.service
│   └── signal-mcp-client.service
└── .local/share/signal-api/         ← Signal-kontodata
```
