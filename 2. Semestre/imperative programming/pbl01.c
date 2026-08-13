#include <stdio.h>

int main() {
    char a, b, c, d, e, f; // tipagem para caracteres
    int n1, n2; // tipagem de inteiros
    float q; // tipagem de numeros com virgula
    int d1, d2, d3, d4, d5, d6; // inteiros para os digitos

    a = getchar(); // pega o primeiro numero do teclado e guarda na variavel 
    getchar(); // segundo pega o ENTER que conta tambem como um digito e descarta fazendo com que o proximo digito a ser lido seja atribuido a variavel
    b = getchar();
    getchar();
    c = getchar();
    getchar();
    d = getchar(); 
    getchar();
    e = getchar();
    getchar();
    f = getchar();
    getchar();

    d1 = a - '0'; // aqui faço uma jogada trocando o meu '5' por um 5 inteiro usando tabela ASCII
    d2 = b - '0';
    d3 = c - '0';
    d4 = d - '0';
    d5 = e - '0';
    d6 = f - '0';

    n1 = d1 * 100 + d2 * 10 + d3;
    n2 = d4 * 100 + d5 * 10 + d6;

    q = (float)n1 / (float)n2;

    printf("%8.3f\n", q);

    return 0;
}
