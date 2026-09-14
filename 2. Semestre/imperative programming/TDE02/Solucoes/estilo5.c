#include <stdio.h>
#include <math.h>

int main() {
    float a, b, c;
    puts("Digite a: ");
    scanf("%f",&a);
    puts("Digite b: ");
    scanf("%f",&b);
    puts("Digite c: ");
    scanf("%f",&c);
    float delta = pow(b,2)-4*a*c;
    printf("%f\n", delta);
    if (delta < 0) {
        puts("Nao existe raiz!");
    }
    else if (delta == 0) {
        puts("Existe uma raiz:");
        float x = -b/(2*a);
        printf("%f\n", x);
    }
    else {
        puts("Existem duas raizes:");
        float raiz = pow(delta,0.5);
        float x = (-b + raiz)/(2*a);
        printf("%f\n", x);
        x = (-b - raiz)/(2*a);
        printf("%f\n", x);
    }
    return 0;
}
