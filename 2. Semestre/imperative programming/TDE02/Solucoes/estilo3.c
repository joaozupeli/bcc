#include <stdio.h>

int main()
{
    float n1, n2;
    double resultado = 0;
    char operador;
    puts("Digite o primeiro operando: ");
    scanf("%f",&n1);
    puts("Digite o segundo operando: ");
    scanf("%f",&n2);
    getchar();
    puts("Digite um operador (+, -, *, /): ");
    operador = getchar();
    switch (operador) {
        case '+':
            resultado = n1 + n2;
            break;
        case '-':
            resultado = n1 - n2;
            break;
        case '*':
            resultado = n1 * n2;
            break;
        case '/':
            resultado = n1 / n2;
            break;
        default:
            puts("Operador inválido");
    }

    printf("Resultado = %.2f\n", resultado);
    return 0;
}
