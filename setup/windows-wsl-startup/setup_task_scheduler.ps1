# setup_task_scheduler.ps1
# Plassering: C:\Users\arne_\setup_task_scheduler.ps1
#
# Kjor dette en gang som administrator for aa opprette
# Task Scheduler-oppgaven automatisk.
#
# Aapne PowerShell som administrator og kjor:
#   Set-ExecutionPolicy Bypass -Scope Process
#   .\setup_task_scheduler.ps1

$taskName    = "Start WSL Signal Bot"
$scriptPath  = "$env:USERPROFILE\start_wsl_bot.ps1"
$psExe       = "powershell.exe"
$psArgs      = "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""

# Sjekk at start_wsl_bot.ps1 finnes
if (-not (Test-Path $scriptPath)) {
    Write-Error "Finner ikke $scriptPath - kopier start_wsl_bot.ps1 dit forst."
    exit 1
}

# Fjern eksisterende oppgave hvis den finnes
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Eksisterende oppgave fjernet."
}

# Definer oppgaven
$action  = New-ScheduledTaskAction -Execute $psExe -Argument $psArgs
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 2)

$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

# Registrer oppgaven
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Starter WSL2 ved palogging slik at Signal MCP-boten starter automatisk via systemd." `
    | Out-Null

Write-Host ""
Write-Host "OK - Task Scheduler-oppgave opprettet: '$taskName'"
Write-Host "   Kjores ved neste palogging."
Write-Host ""
Write-Host "Test at det fungerer ved aa kjore oppgaven manuelt naa:"
Write-Host "   Start-ScheduledTask -TaskName '$taskName'"
