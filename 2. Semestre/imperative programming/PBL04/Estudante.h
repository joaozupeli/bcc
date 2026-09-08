#ifndef ESTUDANTE_H
#define ESTUDANTE_H

#include <stdbool.h>

#define CAPACIDADE 100

typedef struct {
    int matricula;
    float nota_semestral;
    bool aprovado;
} Estudante;

#endif
