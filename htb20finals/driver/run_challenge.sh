#!/bin/sh

qemu-system-x86_64 \
    -s \
    -m 64M \
    -nographic \
    -kernel "./bzImage" \
    -append "console=ttyS0 quiet loglevel=3 oops=panic panic=-1 pti=on kaslr min_addr=4096" \
    -no-reboot \
    -cpu qemu64,+smep,+smap \
    -monitor /dev/null \
    -initrd "./check.cpio" \
   -smp cores=2 \
   -smp threads=1
