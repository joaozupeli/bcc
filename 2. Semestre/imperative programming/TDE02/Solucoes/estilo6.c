#include <stdio.h>

enum Mes_e {JANEIRO, FEVEREIRO, MARCO, ABRIL, MAIO, JUNHO,
    JULHO, AGOSTO, SETEMBRO, OUTUBRO, NOVEMBRO, DEZEMBRO};

enum Dia_e {SEGUNDA, TERCA, QUARTA, QUINTA, SEXTA, SABADO, DOMINGO};

char* meses[] = { "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro" };

char* dias_da_semana[] = { "Segunda-feira", "Terça-feira", "Quarta-feira",
    "Quinta-feira", "Sexta-feira", "Sábado", "Domingo" };

int main()
{
    puts("Meses do ano: ");

    for (int m = JANEIRO;m <= DEZEMBRO;m++)
    {
        printf("\t(%2d) %s\n", m, meses[m]);
    }

    int n_mes;
    puts("Selecione um mês pelo seu número: ");
    scanf("%d",&n_mes);
    enum Mes_e mes_selecionado = (enum Mes_e)n_mes;
    printf("Mês selecionado: %s\n", meses[mes_selecionado]);

    putchar('\n');
    puts("Dias da semana: ");

    for (int d = SEGUNDA;d <= DOMINGO;d++)
    {
        printf("\t(%2d) %s\n", d, dias_da_semana[d]);
    }

    int n_dia;
    puts("Selecione um dia pelo seu número: ");
    scanf("%d",&n_dia);
    enum Dia_e dia_selecionado = (enum Dia_e)n_dia;
    printf("Dia selecionado: %s\n", dias_da_semana[dia_selecionado]);

    putchar('\n');

    if (mes_selecionado == JANEIRO || dia_selecionado == DOMINGO)
    {
        puts("Descansar!\n");
    }
    else
    {
        puts("Trabalhar!\n");
    }

    return 0;
}
