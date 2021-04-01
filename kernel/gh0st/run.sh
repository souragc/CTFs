#! /usr/bin/env bash

if [ -z "$1" ] ; then
	qemu-system-x86_64 -kernel ./tiny.kernel -initrd ./init -m 32 -nographic -append "console=ttyS0"
else
	qemu-system-x86_64 -s -kernel ./tiny.kernel -initrd ./init -m 32 -nographic -append "console=ttyS0"
fi
