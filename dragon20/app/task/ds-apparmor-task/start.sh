mount securityfs -t securityfs /sys/kernel/security

# Workaround for not working "docker run" when using "service docker start" inside docker on ubuntu, because of aufs mounting issue
mkdir /data
mount -t tmpfs tmpfs /data
dockerd --data-root /data 2>/dev/null > /dev/null &
sleep 2

# Actual challenge, you may use just this to test your solution localy
docker run --security-opt "apparmor=docker-default-no-flag" -v /flag.txt:/flag-`xxd -p -l 2 /dev/urandom` registry.gitlab.com/$RUN_ME

