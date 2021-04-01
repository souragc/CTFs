#include <stdio.h>

int main()
{
    setvbuf(stdin,NULL,_IONBF,0);
    setvbuf(stdout,NULL,_IONBF,0);
    setvbuf(stderr,NULL,_IONBF,0);
	char buffer[32];
	printf("It's been fun, but here we are at the final challenge!\n");
	printf("May I know your name?\n");
	scanf("%s", buffer);
	printf("It's been nice meeting you, %s!\n", buffer);
}
