#include <stdio.h>
#include <locale.h>

int main()
{
    setlocale(LC_ALL, "Portuguese");

    char nome[20];
    puts("Digite o seu nome: ");
    scanf("%s", nome);

    int idade = 0;
    puts("Digite a sua idade: ");
    scanf("%d",&idade);

    printf("%s, você tem %d anos.\n", nome, idade);
    return 0;
}
