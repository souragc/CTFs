#include<stdio.h>
#include<stdlib.h>


typedef struct{
    int name;
    char str[32];
}nameer;


void check(const nameer * checker){
    read(0,&checker,sizeof(checker));
    printf("%d", checker->name);
    return;
}

int main(){
    nameer * first = malloc(sizeof(nameer));
    first->name=50;
    check(first);
    return 0;
}
