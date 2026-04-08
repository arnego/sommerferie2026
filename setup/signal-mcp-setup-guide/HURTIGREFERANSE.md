## Hurtigreferanse – Signal MCP Bot (WSL + Podman)

### Daglig bruk
# Status på tjenestene
systemctl --user status signal-cli-rest-api signal-mcp-client

# Se live-logger fra boten
journalctl --user -u signal-mcp-client -f

# Restart begge tjenester
systemctl --user restart signal-cli-rest-api signal-mcp-client

### Signal-registrering (kjør én gang)
# 1. Start containeren manuelt første gang
podman run --name signal-cli-api --replace -p 8080:8080 \
  -v $HOME/.local/share/signal-api:/home/.local/share/signal-cli \
  -e 'MODE=json-rpc' docker.io/bbernhard/signal-cli-rest-api:latest-dev

# 2. Koble til QR-kode (åpne i Windows-nettleser)
#    http://localhost:8080/v1/qrcodelink?device_name=signal-bot

# 3. Registrer Lycamobile-nummer
curl -X POST http://localhost:8080/v1/register/+47DITT-NUMMER

# 4. Verifiser med SMS-kode
curl -X POST http://localhost:8080/v1/register/+47DITT-NUMMER/verifyCode/KODEN

# 5. Sett Registration Lock
curl -X POST http://localhost:8080/v1/accounts/+47DITT-NUMMER/registration-lock \
  -H "Content-Type: application/json" -d '{"pin": "DIN-PIN"}'

### Claude Code på repoet
cd ~/projects/sommerferie2026
claude

### Filplasseringer
# Guide og config:       ~/projects/signal-mcp-client/config.json
# MCP-server:            ~/projects/mcp-servers/sommerferie2026/sommerferie2026_server.py
# Signal-data:           $HOME/.local/share/signal-api/
# Systemd-tjenester:     $HOME/.config/systemd/user/
# Repo:                  ~/projects/sommerferie2026/
