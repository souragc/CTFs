#include<stdio.h>
#include<time.h>


unsigned  long int RANCTX[4];

unsigned long int random(){
    unsigned long int v0;
    v0 = RANCTX[0] - ((RANCTX[1] << 27) | (RANCTX[1] >> 5));
    RANCTX[0] = ((RANCTX[2] << 17) | (RANCTX[2] >> 15)) ^ RANCTX[1];
    RANCTX[1] = RANCTX[3] + RANCTX[2];
    RANCTX[2] = v0 + RANCTX[3];
    RANCTX[3] = v0 + RANCTX[0];
    return RANCTX[3];
}


int main(){
    printf("%ld",time(0));
}
