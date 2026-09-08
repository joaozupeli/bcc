#include <stdio.h>
#include "Relatorio.h"

void imprimir_relatorio(Estudante estudantes[], int quantidade) {
    for (int i = 0; i < quantidade; i++) {
        printf("%d %.2f %s\n",
            estudantes[i].matricula,
            estudantes[i].nota_semestral,
            estudantes[i].aprovado ? "aprovado" : "reprovado");
    }
}
