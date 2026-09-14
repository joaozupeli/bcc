#include <stdio.h>

double calcular_salario_liquido(double salario_bruto, double total_descontos)
{
    return salario_bruto - total_descontos;
}

int main()
{
    double salario_bruto;
    double total_descontos;
    double salario_liquido;

    puts("Digite o salário bruto:");
    scanf("%lf",&salario_bruto);
    puts("Digite o total de descontos:");
    scanf("%lf",&total_descontos);
    salario_liquido = calcular_salario_liquido(salario_bruto, total_descontos);
    printf("O salário líquido é %.2f\n", salario_liquido);
    return 0;
}
