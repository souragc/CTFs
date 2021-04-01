#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

int main(){
    size_t pid = fork();
    if(!pid){
        while(1)
            sleep(2);
    }
    char string[16];
    snprintf(string,16,"/proc/%d/mem",pid);
    FILE * fp =  fopen(string,"r+");
    lseek(3,0x404100,0);
    write(3,"aaaaaa",6);
    return 0;
}
