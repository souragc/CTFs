export DISPLAY=:1
# setup admin data
chown -R admin:admin /home/admin/data
chmod -R 700 /home/admin/data
# RUN guest and admin things
su -c "/bin/bash /exploit.sh" guest &
su -c "/bin/bash /admin.sh" admin &
/bin/bash
