#include<stdio.h>
#include<unistd.h>
int main(){
    int a;
    int bytes=60;
    puts("Give me some input");
    read(0,&a,bytes);
    printf("%s",&a);
    return 0;
}
