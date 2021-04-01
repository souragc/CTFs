Invoke-WebRequest -Uri "https://mms.alliedmods.net/mmsdrop/1.10/mmsource-1.10.7-git971-windows.zip" -OutFile metamod.zip
Invoke-WebRequest -Uri "https://sm.alliedmods.net/smdrop/1.10/sourcemod-1.10.0-git6492-windows.zip" -OutFile sourcemod.zip
Expand-Archive .\metamod.zip .\csgo-ds\csgo
Expand-Archive .\sourcemod.zip .\csgo-ds\csgo
Move-Item .\sq.sp -Destination .\csgo-ds\csgo\addons\sourcemod\scripting
cd .\csgo-ds\csgo\addons\sourcemod\scripting
.\spcomp.exe sq.sp
Move-Item .\sq.smx -Destination ..\plugins\sq.smx

Move-Item \sq_ext.dll \csgo-ds\csgo\addons\sourcemod\extensions\sq.ext.dll
echo $null >> \csgo-ds\csgo\addons\sourcemod\extensions\sq.autoload