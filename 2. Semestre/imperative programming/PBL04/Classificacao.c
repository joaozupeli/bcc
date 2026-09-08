#include "Classificacao.h"

void classificar(Estudante *estudante) {
    if (estudante->nota_semestral >= 7.0f)
        estudante->aprovado = true;
    else
        estudante->aprovado = false;
}
