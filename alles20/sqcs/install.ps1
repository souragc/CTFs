Invoke-WebRequest -Uri "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip" -OutFile steamcmd.zip
Expand-Archive .\steamcmd.zip .\steamcmd
cd .\steamcmd
.\steamcmd.exe +login anonymous +force_install_dir ..\csgo-ds +app_update 740 +quit