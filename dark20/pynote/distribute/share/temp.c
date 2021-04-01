#include<stdio.h>

int main(){
    char * a =malloc(0x60);
    free(a);
    free(a);
    free(a);
    char * b =malloc(0x60);
    strcpy(b,"aaaaaaaa");
    int x;
    scanf("%d",&x);
    return 0;
}
