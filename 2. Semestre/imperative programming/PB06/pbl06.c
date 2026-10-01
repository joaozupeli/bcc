#include <stdio.h>

#define NUMERO_DE_SENSORES 4
typedef enum {JANELA, VENTILADOR, ILUMINACAO, PORTA} Sensor;
char* nome_do_sensor[] = {"JANELA", "VENTILADOR", "ILUMINACAO", "PORTA"};

char* quando_zero[] = {"Fechada", "Desligado", "Desligada", "Fechada"};
char* quando_um[] = {"Aberta", "Ligado", "Ligada", "Aberta"};

unsigned char compor_mensagem(void) {
    unsigned char mensagem = 0;
    int estado;

    for (int i = 0; i < NUMERO_DE_SENSORES; i++) {
        printf("Estado de %s (0 ou 1): ", nome_do_sensor[i]);
        scanf("%d", &estado);

        if (estado == 1)
            mensagem = mensagem | (1 << i);
    }

    return mensagem;
}

void exibir_menagem(unsigned char mensagem) {
    int bit;

    for (int i = 0; i < NUMERO_DE_SENSORES; i++) {
        bit = (mensagem >> i) & 1;

        if (bit == 0)
            printf("%s: %s\n", nome_do_sensor[i], quando_zero[i]);
        else
            printf("%s: %s\n", nome_do_sensor[i], quando_um[i]);
    }
}

int main(void) {
    unsigned char mensagem;

    mensagem = compor_mensagem();
    exibir_menagem(mensagem);

    return 0;
}
