# Escola Politécnica da PUCPR

**Prof. Alcides Calsavara**  
**Programação Imperativa**  
**Prova Teórica – RA1 – abril de 2026**

**Nome completo do aluno:**

## Questão 1 — 2 pontos

Complete os quadros a seguir com a impressão obtida com a execução do programa abaixo. Somente será considerada correta a resposta que estiver integralmente de acordo com o resultado esperado.

A função matemática `sqrt` retorna a raiz quadrada do valor passado como parâmetro, a função `pow` calcula a potência (o primeiro parâmetro é a base, e o segundo é o expoente), a função `log2` calcula o logaritmo na base 2 do valor passado como parâmetro.

**(a)**  
**(b)**

```c
#include <stdio.h>
#include <math.h>
int main()
{
    // Potência: é quando multiplicamos um número por ele mesmo várias vezes. Ex: 2^3 = 2*2*2 = 8.
    // Logaritmo: é o número de vezes que precisamos multiplicar uma base para chegar a outro número.
    // Por exemplo, logaritmo na base 2 de 8 é 3, pois 2*2*2 = 8.
    float x = 16.0;
    double f = 5 * sqrt(x) + 3 * x + 2.05;   // f=70.05
    double g = log2(x) + pow(x, 2); // log2(x) = 4 + pow(x,2)= 256 260
    printf("%.2f\n", f); // quadro (a)
    printf("%.2f\n", g); // quadro (b)
    return 0;
}
```
70.05 ✅
260.00✅

---

## Questão 2 — 3 pontos

    Considere um sistema de execução que aloca as variáveis de um programa na linguagem C de acordo com a política de pilha, sendo que variáveis do tipo `int` e do tipo `float` ocupam quatro bytes, variáveis do tipo `double` ocupam oito bytes e variáveis do tipo `char` ocupam apenas um byte.

Supondo uma alocação contígua (isto é, sem espaços entre variáveis) e considerando que o quadro **(a)** contém o endereço (em decimal) de memória onde está alocada a variável `c` do programa abaixo, complete os quadros **(b)** a **(e)** com os endereços das demais variáveis, de acordo com a ordem de impressão obtida com a execução do programa. Somente será considerada correta a resposta que estiver integralmente de acordo com o resultado esperado.

**(a)** `0x7ffc7f307b4f`  
**(b)**  
**(c)**  
**(d)**

```c
#include <stdio.h>
int main()
{
    int k = 10;
    float f = 5.9f;
    double d = 7.85;
    char c = '#';
    printf("%p\n", &c); // quadro (a)
    printf("%p\n", &d); // quadro (b)
    printf("%p\n", &f); // quadro (c)
    printf("%p\n", &k); // quadro (d)
    return 0;
}
```
(a) 0x7ffc7f307b4f (c)
(b) 0x7ffc7f307b50 (d)
(c) 0x7ffc7f307b58 (f)
(d) 0x7ffc7f307b5c (k)

---

## Questão 3 — 3 pontos

Complete o quadro a seguir com a impressão obtida com a execução do programa abaixo. Somente será considerada correta a resposta que estiver integralmente de acordo com o resultado esperado.

```c
#include <stdio.h>
int main()
{
    char v[] = { 'y', 'r', 'p', 'u', 'h', 'm', 'f', 'k' }; 
    int N = sizeof(v) / sizeof(char);
    for (int i = 1; i < N; i++)
    {
        if (v[i] < v[0]) 
        {
            char aux = v[0]; // aux = p
            v[0] = v[i]; // v[0] = h
            v[i] = aux; // v[i] = p
        }
    }
    putchar(v[0]); // impressão da resposta
    return 0;
}
```
['f', 'y', 'r', 'u', 'p', 'm', 'h', 'k']

---

## Questão 4 — 2 pontos

Complete o quadro a seguir com o valor da variável `x` impressa com a execução do programa abaixo. Somente será considerada correta a resposta que estiver integralmente de acordo com o resultado esperado. Deve-se considerar que as letras do alfabeto estão em sequência contígua na Tabela ASCII.

```c
#include <stdio.h>
int main()
{
    char a = 'A'; char b = 'F'; char c = 'D';
    char* pa = &a; char* pb = &b; char* pc = &c; // aqui ele criou 3 ponteiros que são basicamente os valores de a,b,c sendo apontados em outra variavel
    int x = 0;
    switch (*pc - *pa) // aqui acredito que ele chame esse ponteiro solicitanndo o valor dele eu acho.
    {
        case 1: if (*pc < *pa) x = 1; else x = 2; break; // nesse caso nao roda porque nao cai no case, e roda o swich novamente
        case 2: if (*pc < *pb) x = 3; else x = 4; break; // nesse caso nao roda porque nao cai no case, e roda o swich novamente
        case 3: if (*pb < *pa) x = 5; else x = 6; break; // aqui roda proque o resultado o switch é = 3 entao, x = 6 porque o ponteiro de b não é maior que a.
        default: x = 0;
    }
    printf("%d", x); // impressão da resposta
    return 0;
}

x = 6
```
