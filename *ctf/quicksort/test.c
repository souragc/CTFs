#include<stdio.h>
int main() {
 int m, n, k=0, i, j,temp;
 scanf("%d%d", &m, &n);
 int a[50],b[50];
 for(i=0; i<m; i++) scanf("%d", &a[i]);
 for(i=0; i<n; i++) scanf("%d", &b[i]);
 i=0;j=0;
 for(;j<n;){ 
	for(;i<m;){
  if (a[i] < b[j]) {
   i++;
   }
  else {
   temp=b[j];
   b[j]=a[i];
   a[i]=temp;
   i++;
 
   }}
   a[i]=b[j];
   i=0;
   m++;
   j++;}
 for (int i=0; i<m; i++) printf("%d ", a[i]);
 return 0;
 }

