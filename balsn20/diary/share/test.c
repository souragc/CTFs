#include<stdio.h>
int main(){
    char * a=  malloc(0x20);
    free(a);
    return 0;
}
