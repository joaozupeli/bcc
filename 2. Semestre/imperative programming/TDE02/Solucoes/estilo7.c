#include <stdio.h>
#define TAM 10

int main()
{
    char letras[TAM];

    puts("Digite 10 letras:");

    for (int i = 0;i < TAM;i++)
    {
        printf("letra %d: ", i+1);
        letras[i] = getchar();
        getchar();
    }

    puts("As 10 letras digitadas foram:");

    for (int i = 0;i < TAM;i++)
    {
        putchar(letras[i]);
    }
    putchar('\n');

    puts("Digite uma sequência de, no máximo, 9 letras:");
    scanf("%9s", letras);
    printf("Sequência digitada: %s", letras);
    putchar('\n');

    return 0;
}
