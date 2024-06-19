#include <stdio.h>

int main()
{
    float celsius, fahr;
    int STEP, LOWER, UPPER;

    LOWER = 0;
    UPPER = 300;
    STEP = 20;


    // #define celsius /*celsius temperature */
    // #define fahr /*fahrenhet temperature*/

    for (fahr=0; fahr <= 200; fahr=fahr+STEP)
    {
        printf("%3.0f %6.1f\n", fahr, celsius = 5.0 *(fahr-32.0) / 9);
    }

}
