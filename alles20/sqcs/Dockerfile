FROM mcr.microsoft.com/windows/servercore:ltsc2019
COPY install.ps1 .
RUN powershell -ExecutionPolicy Bypass -File .\install.ps1
COPY install_mod.ps1 .
COPY sq.sp .
COPY sq_ext.dll .
RUN powershell -ExecutionPolicy Bypass -File .\install_mod.ps1
COPY run.ps1 .
COPY flag.txt .
CMD powershell -ExecutionPolicy Bypass -File .\run.ps1
