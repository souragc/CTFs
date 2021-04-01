#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
    read_flag();
    puts("Done with read_flag");
    make_dump();
}

void read_flag(){
    FILE *stream;
    void* ptr;
    void* ptr1;
    void* ptr2;
    int ran;
    
    stream = fopen("flag.txt", "r");
    ptr = malloc(32);
    memset(ptr,'$',32);
    ptr1 = malloc(32);
    ptr2 = malloc(32);
    gets(ptr2);
    
    fread(ptr1, 32, 1, stream);
    puts(ptr1);
    srand(10);
    for(int i =0; i < 64;i++){
        ran = rand();
    }
}

void make_dump(){
    FILE *stream;
    FILE *mem;
    FILE *dw;
    char ptr[100];
    long long int off,endoff;
    long long int heap_off1;
    char* lineptr;
    char* src;
    char dest[13];
    size_t len = 0;
    size_t size = 0;
    size_t heap_size = 0;
    void* mem_mal;
    void* heap_mal;
    char heap_start[13];
    
    stream = fopen("/proc/self/maps", "r");
    fread(ptr, 12, 1, stream);
    off = strtoll(ptr,0,16);
    lineptr = 0;
    do
        getline(&lineptr, &len, stream);
    while ( !strstr(lineptr, "[heap]") );
    puts(lineptr);
    strncpy(heap_start, lineptr, 12);
    puts(heap_start);
    
    heap_off1 = strtoll(heap_start, 0, 16);
    
    src = strchr(lineptr, 45);
    puts("Found Heap Line");
    puts(src);
    if ( src ){
        strncpy(dest, ++src, 12);
        endoff = strtoll(dest, 0, 16);
    }
    puts(dest);
    
    //Calculate the binary + heap
    size = endoff - off;
    
    //calculate the heap size
    heap_size = endoff - heap_off1;
    heap_mal = malloc(heap_size);
    
    //Open mem
    mem = fopen("/proc/self/mem", "r");
    //seek to binary base
    fseek(mem, off, 0);
    //read from binary base to heap end
    fread(mem_mal, size, 1, mem);
    puts("Finished reading mem");
    //read the heap only
    fread(heap_mal, heap_size, 1, mem);
    puts("Finished reading heap");
    fclose(mem);

    //Dump from binary base to heap end.
    dw = fopen("csdump", "w");
    fwrite(mem_mal, size, 1uLL, dw);
    fclose(dw);

    //Dump only the heap
    dw = fopen("hdump", "w");
    fwrite(heap_mal, heap_size, 1uLL, dw);
    fclose(dw);
}