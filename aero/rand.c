#include<stdio.h>
#include<stdlib.h>
#include<time.h>
int main(){
	int r;
	srand(time(0)+232);
	r=rand();
	printf("%d",r);
}
