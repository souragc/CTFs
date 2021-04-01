#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>

void * array[5];
unsigned int count = 0;
void initialize(){
    setvbuf(stdin,NULL,_IONBF,0);
    setvbuf(stdout,NULL,_IONBF,0);
    setvbuf(stderr,NULL,_IONBF,0);
    alarm(60);
}

void getInp(char *ptr, unsigned int size){
    int n = read(0,ptr,size);
    if(n<0){
        puts("Read error");
        exit(0);
    }
    ptr[n-1]='\0';
    return;
}

unsigned int getInt(){
    char buf[20];
    getInp(buf,19);
    return atoi(buf);
}

int printMenu(){
    puts("-----------------------");
    puts("| 1. Add              |");
    puts("| 2. View             |");
    puts("| 3. Delete           |");
    puts("| 4. Exit             |");
    puts("-----------------------");
    printf("Choice >> ");
    return getInt();
}

void addChunk(){
    if(count>=5){
        puts("Limit reached");
        exit(0);
    }
    printf("Enter size >> ");
    unsigned int size = getInt();
    if(size > 0xa0){
        puts("Size too large");
        exit(0);
    }
    array[count] = malloc(size);
    printf("Enter data >> ");
    getInp(array[count],size);
    count++;
    puts("Success");
    return;
}

void viewChunk(){
    printf("Enter index >> ");
    unsigned int idx = getInt();
    if(idx >=5 || !array[idx]){
        printf("Invalid");
        exit(0);
    }
    puts("You data:");
    printf("%s\n",(char*)array[idx]);
    puts("Success");
    return;
}

void deleteChunk(){
    printf("Enter index >> ");
    unsigned int idx = getInt();
    if(idx >=5 || !array[idx]){
        printf("Invalid");
        exit(0);
    }
    free(array[idx]);
    puts("Success");
    return;
}

int main(){
    initialize();
    while(1){
        int option = printMenu();
        switch(option){
            case 1: addChunk();break;
            case 2: viewChunk();break;
            case 3: deleteChunk();break;
            case 4: puts("Bye"); exit(0);
            default: puts("Invalid");
        }
    }
}
