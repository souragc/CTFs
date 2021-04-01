obj-m += vulnmod.o
ccflags-y += ${MY_CFLAGS}
CC += ${MY_CFLAGS}


KDIR="/home/p4wn/challdev/rarfkernel/linux-5.10.17"

all:
		make -C $(KDIR) M=$(PWD) modules
debug:
		make -C $(KDIR) M=$(PWD) modules
		EXTRA_CFLAGS="$(MY_CFLAGS)"
clean:
		make -C $(KDIR) M=$(PWD) clean
