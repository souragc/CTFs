#!/bin/sh
qemu-system-x86_64 \
    -m 256M \
    -kernel ./bzImage \
    -initrd ./check.cpio \
    -append "root=/dev/ram rw console=ttyS0 oops=panic panic=1 nokaslr pti=off quiet" \
    -cpu qemu64,+smep \
    -monitor /dev/null \
    -s \
    -nographic
