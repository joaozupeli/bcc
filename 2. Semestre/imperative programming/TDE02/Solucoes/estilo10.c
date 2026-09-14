#include <stdio.h>

const int MAX_LETRAS = 9;
const int TAMANHO_BUFFER = MAX_LETRAS + 1;
const int DESLOC_NOME = 1;
const int DESLOC_SOBRENOME = 2;

void ler_texto(char texto[])
{
    int i = 0;
    int segue = 1;
    while (i < MAX_LETRAS && segue)
    {
        char c = getchar();
        if (c == '\n')
            segue = 0;
        else
        {
            texto[i] = c;
            i++;
        }
    }
    texto[i] = '\0';
    while (segue)
    {
        char c = getchar();
        if (c == '\n')
            segue = 0;
    }
}

void deslocar(char dest[], char orig[], int qtd)
{
    int i = 0;
    while (orig[i])
    {
        dest[i] = orig[i] + qtd;
        i++;
    }
    dest[i] = '\0';
}

int main()
{
    char primeiro_nome[TAMANHO_BUFFER];
    char sobrenome[TAMANHO_BUFFER];
    char nome_crip[TAMANHO_BUFFER];
    char sobrenome_crip[TAMANHO_BUFFER];
    char nome_desc[TAMANHO_BUFFER];
    char sobrenome_desc[TAMANHO_BUFFER];

    printf("Digite o primeiro nome e tecle ENTER: ");
    ler_texto(primeiro_nome);
    printf("Primeiro nome armazenado: %s\n", primeiro_nome);

    printf("Digite o sobrenome e tecle ENTER: ");
    ler_texto(sobrenome);
    printf("Sobrenome armazenado: %s\n", sobrenome);

    deslocar(nome_crip, primeiro_nome, DESLOC_NOME);
    deslocar(sobrenome_crip, sobrenome, DESLOC_SOBRENOME);

    printf("Primeiro nome criptografado: %s\n", nome_crip);
    printf("Sobrenome criptografado: %s\n", sobrenome_crip);

    deslocar(nome_desc, nome_crip, -DESLOC_NOME);
    deslocar(sobrenome_desc, sobrenome_crip, -DESLOC_SOBRENOME);

    printf("Primeiro nome descriptografado: %s\n", nome_desc);
    printf("Sobrenome descriptografado: %s\n", sobrenome_desc);

    return 0;
}
