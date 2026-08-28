#include <stdio.h>

int main(void) {

    int T,D,M,gap=0,maior_gap=0,atual=0;

    scanf("%d %d %d",&T, &D, &M);

    // varre as refeicoes em ordem cronologica olhando o vao livre ANTES de cada uma
    for (int i=0; i<M; i++){
        scanf("%d", &gap);

        // posso dormir do minuto 'atual' (logo apos a refeicao anterior) ate o minuto da refeicao atual
        if ((gap-atual) > maior_gap)
            maior_gap = gap-atual;

        atual = gap;
    }

    // sobrou o vao entre a ultima refeicao e o fim do voo (se M=0, atual fica 0 e o vao e o voo inteiro)
    if ((D-atual) > maior_gap)
        maior_gap = D-atual;

    if (maior_gap>=T)
        printf("Y\n");
    else
        printf("N\n");

    return 0;
}
