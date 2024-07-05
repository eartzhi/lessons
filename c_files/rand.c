#include <stdio.h>

void main(void)
{
    unsigned long int next;
    unsigned long int x;
    int c = 5;
    
    unsigned long int rand(unsigned long int next)
    {
      next = next * 1103515245 + 12345;
      return (unsigned long int)(next/65536) % 32768;
    }

   unsigned long int srand(unsigned long int seed)
    {
     next = seed;
     return (unsigned long int)next;
    }

    next = srand(10);
    x = rand(next);
    printf("%d", x);

}