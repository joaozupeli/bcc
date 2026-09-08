#include <stdio.h>
#include "Leitura.h"

int ler_dados_dos_estudantes(Estudante estudantes[]) {
    int quantidade;

    scanf("%d", &quantidade);

    if (quantidade > CAPACIDADE)
        quantidade = CAPACIDADE;

    if (quantidade < 0)
        quantidade = 0;

    for (int i = 0; i < quantidade; i++) {
        scanf("%d", &estudantes[i].matricula);
        scanf("%f", &estudantes[i].nota_semestral);
    }

    return quantidade;
}
