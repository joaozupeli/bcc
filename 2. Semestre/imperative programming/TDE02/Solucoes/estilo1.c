#include <stdio.h>

int main()
{
    const char letra = 'H';
    const int vezes = 10;
    for (int i = 1;i <= vezes;i++)
        putchar(letra);
    putchar('\n');

    int valor = vezes;
    while (valor > 0)
    {
        printf("%d ", valor);
        valor--;
    }
    putchar('\n');

    return 0;
}
