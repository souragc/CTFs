# install presnetation software
sudo dpkg -i /home/admin/data/softmaker-freeoffice-2018_980-01_amd64.deb
echo 'instalation done'
# prepare presentation
/usr/bin/presentations18free /home/admin/data/flag.prdx &
sleep 5
wnd=`xdotool search --name "User interface"`
xdotool key --window "$wnd"  Return
sleep 1000
