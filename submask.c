#include <stdio.h>

int main(){
int m = 0b101;
int s = m;
printf("s-1=%d s=%d \n",(s-1),s);
for (int s=m; ; s=(s-1)&m) {
 printf("s-1=%d s=%d \n",(s-1),s);
 if (s==0)  break;
}
return s;
}
int main();