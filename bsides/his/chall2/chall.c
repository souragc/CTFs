#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include<string.h>

int main()
{
    unsigned char vuln[32];
    unsigned char buffer[64];
    time_t t;
    srand((unsigned) time(&t));
    char buf[10];
    printf("Enter your name : ");
    scanf("%9s",buf);
    printf(buf);
    scanf("%s",buffer);
    memcpy(vuln, buffer, sizeof(buffer));
    for(int i = 0; i < strlen(buffer); i++)
        vuln[i] = ((rand()%100) + vuln[i])%255;
    puts("Got the job done, boss!\n");
    return 0;
}
