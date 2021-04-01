#include<stdio.h>
#include<stdlib.h>
int main(){
    char * ptr=malloc(0x500);
    char * ptr2 = malloc(10);
    int m;
    scanf("%d",&m);

    free(ptr);
    ptr=malloc(0x500);
    return 0;
}
