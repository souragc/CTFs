#include <stdio.h>
#include <stdlib.h>

int main(){
    free(malloc(10));
    return 0;
}
