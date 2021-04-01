URL=https://www.freeoffice.com/download.php?filename=https://www.softmaker.net/down/softmaker-freeoffice-2018_980-01_amd64.deb
DEST=task-env/softmaker-freeoffice-2018_980-01_amd64.deb
[ -f $DEST ] || wget $URL -O $DEST
docker build ds-desktop-enviroment -t ds-desktop-enviroment
