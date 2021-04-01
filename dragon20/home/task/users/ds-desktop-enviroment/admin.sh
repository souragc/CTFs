cd /home/admin
export DISPLAY=:1
export LC_ALL=en_US.UTF-8
xvfb-run -n 1 -s "-screen 0 1920x1080x24" /bin/bash /admin-ui.sh &
