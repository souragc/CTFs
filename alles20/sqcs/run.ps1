cd csgo-ds
.\srcds.exe -game csgo -port $env:PORT -console -insecure -usercon +game_type 0 +game_mode 1 +mapgroup mg_bomb +map de_dust2 +sv_setsteamaccount $env:TOKEN +con_logfile log.log +sv_password $env:PASSWD +sv_tags hidden +sv_hibernate_when_empty 0
while (!(Test-Path "csgo\log.log")) { Start-Sleep 1 }
Get-Content csgo\log.log -wait