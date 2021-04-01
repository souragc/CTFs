sleep 1
[ -z "${START_VNC}" ] || x11vnc -display :1 -bg -forever -nopw -listen 0.0.0.0 -xkb
gnome-panel &
metacity &
/usr/bin/dbus-launch /usr/lib/gnome-settings-daemon/gsd-housekeeping &
sleep 5
/usr/bin/dbus-launch gnome-terminal &
/usr/bin/dbus-launch gnome-terminal -- /home/admin/data/admin_action.sh &
sleep 100000
