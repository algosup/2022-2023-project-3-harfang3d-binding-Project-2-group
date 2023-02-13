/* isalnum example */
#include <stdio.h>
#include "ctype.h"

#ifdef _WIN32
__declspec(dllexport)
#endif

int main ()
{
  int i;
  char str[]="c3po...";
  i=0;
  while (isalnum(str[i])) i++;
  printf ("The first %d characters are alphanumeric.\n",i);
  return 0;
}