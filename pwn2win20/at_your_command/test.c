#include<stdio.h>
int main(){
    char s[0x10];
    fgets(s,16,stdin);
    printf("%d\n",atoll(s));
    return 0;
}
