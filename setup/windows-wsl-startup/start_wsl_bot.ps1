# start_wsl_bot.ps1
# Plassering: C:\Users\DITTBRUKERNAVN\start_wsl_bot.ps1
#
# Starter WSL slik at systemd booter og tjenestene
# (signal-cli-rest-api og signal-mcp-client) starter automatisk.
#
# Kjøres ved Windows-pålogging via Task Scheduler.

# Vent litt til nettverket er oppe
Start-Sleep -Seconds 5

# Start WSL – systemd tar seg av resten
wsl --exec sleep 3

# Valgfritt: logg oppstartstidspunkt
$logFile = "$env:USERPROFILE\wsl_bot_startup.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logFile -Value "$timestamp – WSL startet"
