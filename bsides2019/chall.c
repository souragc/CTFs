#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>

typedef struct message{
    char topic[24];
    char * body;
    unsigned int size;
}message;

message * table[10];

int getinp(char* ptr, int size)
{
  int ret = read(0,ptr,size-1);
  if (ret<0)
    exit(0);
  ptr[ret-1]='\0';
  return ret-1;
}

int getint()
{
  char buf[30];
  getinp(buf,30);
  return atoi(buf);
}

void initialize(){
	alarm(60);
	setvbuf(stdout,NULL,2,0);
	setvbuf(stdin,NULL,2,0);
}

void menu(){
    puts("--------------------");
    puts("1. Add");
    puts("2. Edit");
    puts("3. Delete");
    puts("4. View");
    puts("5. Exit");
    puts("--------------------");
    printf(">>");
    return;
}

void add(){
    puts("Enter the index");
    int index=getint();
    if(index <0 || index >=10){
        puts("Invalid index");
        return;
    }
    message* adding=(message*)malloc(sizeof(message));
    puts("Enter the topic");
    getinp(adding->topic,24);
    puts("Enter the size of body");
    int body_size=getint();
    if(body_size<=0  || body_size>1000){
        puts("The size entered is not valid");
        return;
    }
    adding->size=body_size;
    adding->body=(char*)malloc(adding->size);
    puts("Enter the body");
    getinp(adding->body,adding->size);
    table[index]=adding;
    puts("Message addition successfull");
    return;
}

void edit(){
    puts("Enter the index");
    int index=getint();
    if(index>=0 && index<10 && table[index]){
        message* editing=table[index];
        puts("Enter the new topic");
        getinp(editing->topic,24);
        puts("Enter the new body");
        getinp(editing->body,editing->size);
        puts("Message editing successfull");
        return;
    }
    else{
        puts("Invalid index");
        return;
    }
}

void delete(){
    puts("Enter the index");
    int index=getint();
    if(index>=0 && index<10 && table[index]){
        message * deleting=table[index];
        free(deleting->body);
        free(deleting);
        puts("Message deleting successfull");
        return;
    }
    else{
        puts("Invalid index");
        return;
    }
}

void view(){
    puts("Enter the index");
    int index=getint();
    if(index>=0 && index<10 && table[index]){
        printf("Topic : ");
        printf("%s\n",table[index]->topic);
        printf("Body : ");
        printf("%s\n",table[index]->body);
        puts("Message viewing successfull");
        return;
    }
    else{
        puts("Invalid index");
        return;
    }
}

int main(){
    initialize();
    puts("Welcome to messsage saving service.");
    while(1){
        puts("Please make a selection");
        menu();
        switch(getint()){
            case 1:add();
                   break;
            case 2:edit();
                   break;
            case 3:delete();
                   break;
            case 4:view();
                   break;
            case 5:exit(0);
                   break;
            default: puts("Invalid choice");
        }
    }
}
