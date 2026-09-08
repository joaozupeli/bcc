#include "Estudante.h"
#include "Leitura.h"
#include "Classificacao.h"
#include "Relatorio.h"

int main(void) {
    Estudante estudantes[CAPACIDADE];
    int quantidade;

    quantidade = ler_dados_dos_estudantes(estudantes);

    for (int i = 0; i < quantidade; i++)
        classificar(&estudantes[i]);

    imprimir_relatorio(estudantes, quantidade);

    return 0;
}
