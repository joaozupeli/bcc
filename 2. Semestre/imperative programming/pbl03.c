#include <stdio.h>
#define MAX_TURMAS 1000
#define MAX_FRUTAS 1000


int main(void) {
    int turmas, frutas, maiorPessoas, pessoasEscola = 0;

    printf("Digite quantas frutas e turmas terão, respectivamente: ");
    scanf("%d %d",&frutas, &turmas);

    if (frutas > MAX_FRUTAS || turmas > MAX_TURMAS){
        printf("Número de frutas/turmas excedeu o número máximo de 1000\n");
        return 1;
    }

    int calculoTurmas[frutas][turmas];

    for (int i = 0; i < frutas; i++) {
        for (int j = 0; j < turmas; j++) {
            printf("Digite quantos alunos da turma %d gostam da fruta %d: ", j+1,i+1);
            scanf("%d", &calculoTurmas[i][j]);
        }
    }

    for (int j = 0; j < turmas; j++) {
        maiorPessoas=0;
        for (int i = 0; i < frutas; i++) {
            if (calculoTurmas[i][j] > maiorPessoas) {
                maiorPessoas = calculoTurmas[i][j];
            }
        }
        if (maiorPessoas <= 0) {
            maiorPessoas = 1;
        }
        pessoasEscola += maiorPessoas;
    }


    for (int i = 0; i<frutas; i++) {
        for (int j = 0; j < turmas; j++) {
            printf("%d \t", calculoTurmas[i][j]);
        }
        putchar('\n');
    }

    printf("%d\n", pessoasEscola);




    return 0;
}